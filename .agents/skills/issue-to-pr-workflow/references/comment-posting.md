# Issue・PRコメントの投稿形式

## 改行を保持する

レビューコメントはGitHubが解釈するMarkdownとして投稿する。表、見出し、段落の改行が表示に必要なため、本文は実際の改行を含むMarkdownファイルから渡す。

```zsh
gh issue comment <issue-number> --repo <owner>/<repo> --body-file <comment-file>
gh pr review <pr-number> --repo <owner>/<repo> --comment --body-file <comment-file>
```

`comment-file`は、コメント投稿前に内容を確認できる一時ファイルまたはリポジトリのレビュー成果物とする。投稿後はGitHub上で表、見出し、段落が意図どおりに表示されることを確認する。

## 禁止事項

- JSON文字列化した本文をそのまま`--body`へ渡さない。`\\n`が実際の改行へ変換されず、GitHub上に文字列として表示されることがある。
- JavaScriptやシェルの文字列エスケープに依存してMarkdown本文を組み立てない。
- 外側のコードフェンスでレビュー本文全体を囲まない。
- トークン、device code、認証情報をコメント本文へ含めない。

## 投稿前チェック

1. 本文をファイルとして読み、改行、表、見出し、空行を確認する。
2. `rg '\\\\n' <comment-file>`で、意図しないリテラルの`\\n`が含まれていないことを確認する。コード例など意図したものは除外する。
3. 投稿後にGitHubの表示を確認し、崩れている場合は同じコメントを追加せず、既存のIssueコメントを編集して修復する。
4. 送信済みのPRレビューはGitHub APIで本文を編集できない場合がある。その場合は、古いレビューを`OUTDATED`として折りたたみ、正しいMarkdownのIssueコメントを1件だけ追加して修復内容を明示する。
