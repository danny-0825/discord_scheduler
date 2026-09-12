# コードマップ

Obsidianではコードファイルも同じVault内のファイルとして参照できます。`showUnsupportedFiles`を有効にしているため、ファイルエクスプローラーからDartファイルを確認できます。編集や詳細なコード作業は、普段のエディターを使用してください。

## 主要ファイル

- [ルートハンドラー](../../routes/index.dart) — `/`へのレスポンスを定義
- [ルートハンドラーのテスト](../../test/routes/index_test.dart) — ルートの期待動作を検証
- [依存関係・SDK設定](../../pubspec.yaml) — Dart SDKとパッケージを定義

## ドキュメントからコードを確認する流れ

1. このページのリンクから対象ファイルを開く
2. 実装を変更した場合は、関連するテストとドキュメントを更新する
3. `dart format --output=none --set-exit-if-changed .`、`dart analyze`、`dart test`を実行する
