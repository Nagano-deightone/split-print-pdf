# CLAUDE.md - 開発ガイド

このファイルは、Claude Codeがこのプロジェクトで作業する際のガイダンスを提供します。

## プロジェクト概要

縦長PDFを標準的なA4サイズ（210mm × 297mm）のページに分割して印刷可能な形式に変換するPython CLIツール。

## プロジェクト構造

```
split-print/
├── split_print/
│   ├── __init__.py      # パッケージ初期化
│   ├── cli.py           # CLIエントリーポイント（Click使用）
│   ├── splitter.py      # PDF分割ロジック（pypdf使用）
│   └── constants.py     # 定数定義（A4サイズ等）
├── tests/               # テスト（未実装）
├── requirements.txt     # 依存関係
├── setup.py            # パッケージ設定
├── README.md           # ユーザー向けドキュメント
└── CLAUDE.md           # このファイル
```

## 技術スタック

### コアライブラリ
- **pypdf (>=3.0.0)**: PDF操作（読み込み、ページ分割、新規PDF作成）
- **click (>=8.0.0)**: CLIインターフェース構築

### 要件
- **Python 3.8+**: 型ヒント対応

## 開発環境セットアップ

```bash
cd /Users/naganoaki/claude-workspace/split-print

# 仮想環境を作成
python -m venv venv

# 仮想環境をアクティベート
source venv/bin/activate  # macOS/Linux

# 開発モードでインストール
pip install -e .
```

## 開発コマンド

### パッケージのインストール

```bash
# 開発モードでインストール（ソースコード変更が即座に反映）
pip install -e .

# 通常インストール
pip install .
```

### CLIコマンドの実行

```bash
# インストール後
split-print input.pdf -o output.pdf -v

# または、直接モジュールとして実行
python -m split_print.cli input.pdf -o output.pdf -v
```

### テストの実行（将来実装予定）

```bash
pytest tests/
```

## アーキテクチャ

### 主要コンポーネント

#### 1. constants.py
PDF操作で使用する定数を定義：
- A4サイズ（ポイント単位）
- mm→ポイント変換定数

#### 2. splitter.py
PDF分割のコアロジック：

**PDFSplitterクラス:**
- `split_pdf()`: メインの分割関数
  - PDFの各ページを読み込み
  - 高さがA4を超える場合、縦方向に分割
  - 横幅は元のまま維持
  - オーバーラップオプションをサポート

**分割アルゴリズム:**
1. 元のPDFの各ページをループ
2. ページ高さ > A4高さの場合：
   - 分割数 = `ceil(ページ高さ / A4高さ)`
   - 各セクションを新しいページとしてクロップ
   - PDF座標系（左下原点、y軸上向き）に注意
3. A4以下のページはそのまま追加

#### 3. cli.py
Clickを使ったCLIインターフェース：

**コマンド構造:**
```
split-print <input.pdf> [options]
```

**オプション:**
- `-o, --output`: 出力ファイル名
- `--overlap`: ページ間オーバーラップ（mm）
- `-v, --verbose`: 詳細ログ

### PDF座標系の重要ポイント

- **原点**: 左下（通常の画像処理とは異なる）
- **y軸**: 上向き
- **MediaBox**: `[llx, lly, urx, ury]` 形式（左下x, 左下y, 右上x, 右上y）
- **クロップ**: `mediabox.lower_left` と `mediabox.upper_right` を設定

### ページ分割の計算

縦長ページを上から下に向かって分割する場合：

```python
# split_index = 0 (一番上のセクション)
lower_y = original_height - ((split_index + 1) * page_height)
upper_y = original_height - (split_index * page_height)

# split_index = 1 (2番目のセクション)
lower_y = original_height - 2 * page_height
upper_y = original_height - 1 * page_height
```

## コーディング規約

- 型ヒントを使用（Python 3.8+）
- docstringはGoogle形式
- エラーハンドリングを適切に実装
- verbose フラグで詳細ログを出力

## テストケース（将来実装予定）

### 基本機能
- [ ] A4サイズ以下のPDF（分割不要）
- [ ] 2ページ分の高さのPDF（2ページに分割）
- [ ] 非常に長いPDF（多数ページに分割）

### エッジケース
- [ ] 空のPDF
- [ ] 破損したPDF
- [ ] 横向きのPDF
- [ ] パスワード保護されたPDF

### オプション機能
- [ ] カスタム出力パス
- [ ] オーバーラップ機能
- [ ] verbose モード

## トラブルシューティング

### pypdf のインポートエラー
```bash
# pypdf をインストール
pip install pypdf
```

### CLIコマンドが見つからない
```bash
# setup.py から再インストール
pip install -e .
```

### PDF が正しく分割されない
- verbose モード（`-v`）で詳細ログを確認
- 入力PDFのページサイズを確認（PyPDF2等のツールで）

## 将来の拡張案

- [ ] A4以外のページサイズ対応（Letter、B5等）
- [ ] 横幅の自動調整オプション
- [ ] 複数PDFの一括処理
- [ ] GUI版の開発
- [ ] プログレスバー表示
- [ ] プレビュー機能
- [ ] テストスイートの実装

## 参考リンク

- [pypdf ドキュメント](https://pypdf.readthedocs.io/)
- [Click ドキュメント](https://click.palletsprojects.com/)
- [PDF座標系](https://www.adobe.com/content/dam/acom/en/devnet/pdf/pdfs/PDF32000_2008.pdf)
