# Split-Print

縦に長いPDFを標準的なA4サイズ（210mm × 297mm）のページに分割して、印刷可能な形式に変換するPython CLIツールです。

## 特徴

- 📄 縦長PDFをA4サイズのページに自動分割
- 🖨️ 印刷しやすい標準サイズに変換
- 🔧 シンプルで使いやすいCLIインターフェース
- 🔄 オプションでページ間のオーバーラップ設定可能
- 📦 複数ファイルの一括処理に対応
- 📊 処理結果のサマリー表示

## インストール

### 開発モードでのインストール（推奨）

```bash
cd /Users/naganoaki/claude-workspace/split-print
python -m venv venv
source venv/bin/activate  # macOS/Linux
# または
venv\Scripts\activate  # Windows

pip install -e .
```

### 通常のインストール

```bash
pip install .
```

## 使い方

### 単一ファイルの処理

```bash
split-print input.pdf
```

これにより、`input_split.pdf` という名前で分割されたPDFが作成されます。

### 複数ファイルの一括処理

```bash
# 複数のファイルを指定
batch-split-print file1.pdf file2.pdf file3.pdf

# ワイルドカード使用
batch-split-print ~/Downloads/*.pdf

# 出力先フォルダを指定
batch-split-print *.pdf -o ~/Desktop/output/
```

### 出力ファイル名を指定

```bash
split-print input.pdf -o output.pdf
```

### ページ間にオーバーラップを追加

ページをつなぎ合わせる際のガイドとして、5mmのオーバーラップを追加：

```bash
split-print input.pdf --overlap 5
```

### 詳細ログを表示

```bash
split-print input.pdf -v
```

### 全オプションを確認

```bash
split-print --help
```

## コマンドラインオプション

### split-print（単一ファイル処理）

| オプション | 説明 |
|-----------|------|
| `INPUT_FILE` | 分割する入力PDFファイル（必須） |
| `-o, --output PATH` | 出力ファイルのパス（デフォルト: `{input}_split.pdf`） |
| `--overlap FLOAT` | ページ間のオーバーラップ（mm単位、デフォルト: 0） |
| `-v, --verbose` | 詳細ログを表示 |
| `--help` | ヘルプメッセージを表示 |

### batch-split-print（一括処理）

| オプション | 説明 |
|-----------|------|
| `INPUT_FILES...` | 分割する入力PDFファイル（複数指定可能） |
| `-o, --output-dir PATH` | 出力ディレクトリ（デフォルト: 入力ファイルと同じ場所） |
| `--overlap FLOAT` | ページ間のオーバーラップ（mm単位、デフォルト: 0） |
| `-v, --verbose` | 詳細ログを表示 |
| `--continue-on-error` | エラーが発生しても処理を続行 |
| `--help` | ヘルプメッセージを表示 |

## 動作原理

1. 入力PDFの各ページの高さを確認
2. A4の高さ（297mm = 841.89pt）を超えるページを検出
3. 縦方向に必要な数だけページを分割
4. 各分割ページをA4サイズのページとして新しいPDFに追加
5. 元のページの横幅は維持（A4幅に収まらない場合もそのまま）

## 技術仕様

- **ページサイズ**: A4 (210mm × 297mm = 595.28pt × 841.89pt)
- **PDF座標系**: 左下が原点、y軸は上向き
- **使用ライブラリ**:
  - pypdf: PDF操作
  - click: CLIインターフェース

## ユースケース

- ウェブページをPDF化したものを印刷可能なサイズに分割
- スクロールキャプチャで作成した縦長スクリーンショットPDFを分割
- 縦に長いドキュメントを複数のA4ページに分割して印刷

## 制限事項

- 横幅はA4幅に自動調整されません（元の幅を維持）
- テキストの再配置は行いません（純粋なページ分割のみ）
- 双方向（縦横両方）の分割には対応していません

## ライセンス

MIT License

## 開発

開発に関する詳細は [CLAUDE.md](CLAUDE.md) を参照してください。
