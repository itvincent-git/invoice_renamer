# Invoice Renamer

## Description
A Python tool that automatically renames invoice files based on their content using OCR technology. The tool extracts the invoice date and amount from PDF/JPG files and renames them in a standardized format: `YYYYMMDD_AMOUNT元.pdf`.

### Features
- Supports PDF and JPG/JPEG file formats
- Extracts invoice date and amount using PaddleOCR
- Processes single files or entire directories
- Creates renamed files in a separate 'rename' directory
- Supports Chinese invoice format

## Prerequisites
- Python 3.11 or higher
- uv package manager
- macOS (for current installation instructions)

## Installation

### 1. Install uv (Package Manager)
```sh
pip install uv
```

### 2. Clone and Setup Project
```sh
git clone <repository-url>
cd invoice_renamer
uv venv
uv sync
```

### 3. Install PaddlePaddle OCR Components

#### Install PaddlePaddle Core (macOS)
```sh
uv pip install paddlepaddle==3.0.0rc1 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/
```

#### Install PaddleOCR
```sh
uv add paddleocr
```

#### Install Additional Dependencies
```sh
brew install ccache
```

## Usage

### Process Single File
```sh
python main.py path/to/invoice.pdf
```

### Process Entire Directory
```sh
python main.py path/to/directory
```

### Output Format
Files will be renamed to: `YYYYMMDD_AMOUNT元.pdf`
Example: `20250315_683.00元.pdf`

## Requirements
See [pyproject.toml](pyproject.toml) for detailed dependencies:
- paddleocr >= 2.10.0
- pdf2image >= 1.17.0
- argparse >= 1.4.0

## References
- [PaddleOCR GitHub Repository](https://github.com/PaddlePaddle/PaddleOCR)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.