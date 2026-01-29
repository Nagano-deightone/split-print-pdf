# 使用例

## セットアップ

```bash
cd /Users/naganoaki/claude-workspace/split-print

# 仮想環境を作成（初回のみ）
python3 -m venv venv

# 仮想環境をアクティベート
source venv/bin/activate  # macOS/Linux

# パッケージをインストール
pip install -e .
```

## 基本的な使い方

### 1. 最もシンプルな使い方

```bash
split-print long-document.pdf
```

出力: `long-document_split.pdf`

### 2. 出力ファイル名を指定

```bash
split-print long-document.pdf -o printable.pdf
```

出力: `printable.pdf`

### 3. 詳細ログを表示

```bash
split-print long-document.pdf -v
```

出力例:
```
[INFO] Reading PDF: long-document.pdf
[INFO] Processing 1 pages from input PDF
[INFO] Page 1: 595.3pt × 2525.7pt
[INFO]   → Splitting into 3 pages
[INFO]     Split 1/3: y=1683.8 to 2525.7 (height=841.9pt)
[INFO]     Split 2/3: y=841.9 to 1683.8 (height=841.9pt)
[INFO]     Split 3/3: y=0.0 to 841.9 (height=841.9pt)
[INFO] Writing output to: long-document_split.pdf
[INFO] Total pages created: 3
[INFO] Done!
✓ PDF split successfully!
```

### 4. ページ間にオーバーラップを追加

つなぎ合わせやすくするため、5mmのオーバーラップを追加:

```bash
split-print long-document.pdf --overlap 5
```

## 実践例

### ウェブページをPDFにして分割

```bash
# 1. ブラウザでウェブページを「PDFとして保存」
# 2. 保存されたPDFを分割
split-print webpage.pdf -o webpage-printable.pdf -v
```

### 複数のPDFを一括処理

```bash
# Bashのforループを使用
for pdf in *.pdf; do
  split-print "$pdf" -o "printable_${pdf}"
done
```

### Pythonスクリプトから使用

```python
from split_print.splitter import split_pdf_file

# 基本的な使い方
split_pdf_file('input.pdf', 'output.pdf')

# オプション付き
split_pdf_file(
    input_path='input.pdf',
    output_path='output.pdf',
    overlap_mm=5.0,
    verbose=True
)
```

## トラブルシューティング

### コマンドが見つからない

```bash
# 仮想環境がアクティブか確認
which split-print

# 再インストール
pip install -e .
```

### PDFが正しく分割されない

```bash
# 詳細ログで確認
split-print input.pdf -v

# 入力PDFの情報を確認
python3 -c "from pypdf import PdfReader; r = PdfReader('input.pdf'); print(f'Pages: {len(r.pages)}'); [print(f'Page {i+1}: {float(p.mediabox.width):.1f}pt × {float(p.mediabox.height):.1f}pt') for i, p in enumerate(r.pages)]"
```

## ヒント

- A4サイズは 595.28pt × 841.89pt（210mm × 297mm）
- 1ポイント = 1/72 インチ = 約0.353mm
- オーバーラップは印刷後につなぎ合わせる際に便利
- 元のPDFの横幅は維持されます（A4幅を超える場合も）
