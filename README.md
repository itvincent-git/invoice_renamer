# Invoice Renamer
## Description
A tool to rename invoice files.
It will rename the invoice file to the invoice amount and the invoice date.

## Usage
```sh
uv run invoice_renamer.py test.pdf
```

## Install
### Install uv
```sh
pip install uv
```

### Install dependencies
```sh
uv venv
uv sync
```

### Install paddlepaddle for OCR
macOS:
```sh
uv pip install paddlepaddle==3.0.0rc1 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/
```
Detail to read: [PaddlePaddle/PaddleOCR)](https://github.com/PaddlePaddle/PaddleOCR)

### Install paddleocr
```sh
uv add paddleocr
```

### Install ccache
```sh
brew install ccache
```