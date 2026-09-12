#!/usr/bin/env python3
"""Search Markdown documents with a small dependency-free BM25 implementation."""

from __future__ import annotations

import argparse
import json
import math
import re
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


TOKEN_RE = re.compile(r"[A-Za-z0-9_]+|[\u3040-\u30ff\u3400-\u9fff]+|[^\W\d_]+", re.UNICODE)
SKIP_DIRS = {".git", ".dart_tool", "build", "__pycache__"}


def tokenize(text: str) -> list[str]:
    normalized = unicodedata.normalize("NFKC", text).casefold()
    tokens: list[str] = []
    for match in TOKEN_RE.finditer(normalized):
        token = match.group(0)
        tokens.append(token)
        if any("\u3040" <= char <= "\u9fff" for char in token) and len(token) > 1:
            tokens.extend(token[index : index + 2] for index in range(len(token) - 1))
    return tokens


@dataclass(frozen=True)
class Document:
    path: Path
    text: str


@dataclass(frozen=True)
class Result:
    path: str
    score: float
    heading: str
    snippet: str


class BM25:
    def __init__(self, documents: Iterable[Document], k1: float = 1.5, b: float = 0.75):
        if k1 < 0:
            raise ValueError("k1 must be non-negative")
        if not 0 <= b <= 1:
            raise ValueError("b must be between 0 and 1")
        self.documents = list(documents)
        self.k1 = k1
        self.b = b
        self.tokens = [tokenize(document.text) for document in self.documents]
        self.lengths = [len(tokens) for tokens in self.tokens]
        self.average_length = sum(self.lengths) / len(self.lengths) if self.lengths else 0.0
        document_frequency: defaultdict[str, int] = defaultdict(int)
        for tokens in self.tokens:
            for token in set(tokens):
                document_frequency[token] += 1
        self.idf = {
            token: math.log(1 + (len(self.documents) - frequency + 0.5) / (frequency + 0.5))
            for token, frequency in document_frequency.items()
        }

    def search(self, query: str, limit: int = 10) -> list[tuple[Document, float]]:
        if not query.strip() or not self.documents or limit <= 0:
            return []
        query_tokens = set(tokenize(query))
        ranked: list[tuple[Document, float]] = []
        for document, tokens, length in zip(self.documents, self.tokens, self.lengths):
            counts = Counter(tokens)
            score = 0.0
            for token in query_tokens:
                frequency = counts.get(token, 0)
                if not frequency:
                    continue
                normalization = 1 - self.b
                if self.average_length:
                    normalization += self.b * length / self.average_length
                score += self.idf.get(token, 0.0) * (
                    frequency * (self.k1 + 1) / (frequency + self.k1 * normalization)
                )
            if score > 0:
                ranked.append((document, score))
        ranked.sort(key=lambda item: (-item[1], item[0].path.as_posix()))
        return ranked[:limit]


def collect_documents(roots: Iterable[Path]) -> list[Document]:
    paths: set[Path] = set()
    for root in roots:
        if root.is_file() and root.suffix.lower() == ".md":
            paths.add(root)
        elif root.is_dir():
            for path in root.rglob("*.md"):
                if not any(part in SKIP_DIRS for part in path.parts):
                    paths.add(path)
    return [Document(path, path.read_text(encoding="utf-8")) for path in sorted(paths)]


def heading_and_snippet(text: str, query: str) -> tuple[str, str]:
    query_tokens = set(tokenize(query))
    heading = ""
    best_line = ""
    for line in text.splitlines():
        if line.startswith("#") and not heading:
            heading = line.lstrip("# ").strip()
        if query_tokens.intersection(tokenize(line)) and not best_line:
            best_line = " ".join(line.strip().split())
    snippet = best_line or " ".join(text.split())[:160]
    return heading, snippet[:200]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="+", help="検索語")
    parser.add_argument("--root", action="append", type=Path, help="検索対象root（複数指定可）")
    parser.add_argument("--limit", type=int, default=10, help="最大結果数")
    parser.add_argument("--k1", type=float, default=1.5)
    parser.add_argument("--b", type=float, default=0.75)
    parser.add_argument("--json", action="store_true", help="JSONで出力")
    args = parser.parse_args()
    roots = args.root or [Path("docs")]
    query = " ".join(args.query)
    engine = BM25(collect_documents(roots), k1=args.k1, b=args.b)
    results = []
    for document, score in engine.search(query, limit=args.limit):
        heading, snippet = heading_and_snippet(document.text, query)
        results.append(Result(document.path.as_posix(), score, heading, snippet))
    if args.json:
        print(json.dumps([result.__dict__ for result in results], ensure_ascii=False, indent=2))
    else:
        for result in results:
            print(f"{result.score:.4f}\t{result.path}\t{result.heading}\t{result.snippet}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
