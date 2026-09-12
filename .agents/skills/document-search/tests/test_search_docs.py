import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "search_docs.py"
SPEC = importlib.util.spec_from_file_location("search_docs", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules["search_docs"] = MODULE
SPEC.loader.exec_module(MODULE)


class SearchDocsTest(unittest.TestCase):
    def test_japanese_bigram_query_ranks_matching_document(self):
        documents = [
            MODULE.Document(Path("generic.md"), "これは一般的なメモです"),
            MODULE.Document(Path("requirements.md"), "要件定義と受入条件を整理します"),
        ]
        results = MODULE.BM25(documents).search("要件定義")
        self.assertEqual(results[0][0].path.name, "requirements.md")

    def test_empty_query_and_limit_are_safe(self):
        engine = MODULE.BM25([MODULE.Document(Path("one.md"), "内容")])
        self.assertEqual(engine.search(""), [])
        self.assertEqual(engine.search("内容", limit=0), [])

    def test_collect_documents_skips_generated_directories(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs").mkdir()
            (root / ".dart_tool").mkdir()
            (root / "docs" / "good.md").write_text("検索対象", encoding="utf-8")
            (root / ".dart_tool" / "bad.md").write_text("検索対象", encoding="utf-8")
            paths = [document.path.name for document in MODULE.collect_documents([root])]
            self.assertEqual(paths, ["good.md"])


if __name__ == "__main__":
    unittest.main()
