# Beijing Math Question Extractor Skill

## Purpose
Extract Chinese math questions from Beijing placement exam PDFs using free Tesseract OCR (no API limits).

## Features
- Free OCR using Tesseract (no quota limits)
- Chinese text recognition (chi_sim)
- Automatic question parsing
- Progress tracking
- Works offline

## Usage

### Extract Sample Pages
```bash
source .venv/bin/activate
python extract_beijing_complete.py
```

### Extract All Pages (5-256)
```python
from extract_beijing_complete import extract_all_pages

pdf_path = 'data/北京各区分班考试真题集—数学 .pdf'
output_json = 'output/beijing_math_all.json'

# Extract all pages (skip cover 1-4)
extract_all_pages(pdf_path, 5, 256, output_json)
```

### Extract Specific Range
```python
# Pages 50-100
extract_all_pages(pdf_path, 50, 100, 'output/batch_50_100.json')
```

## Output Format

```json
[
  {
    "page": 5,
    "raw_text": "完整OCR文本...",
    "questions": [
      {
        "number": "5",
        "content": "在所有的质数中偶数的个数有( )",
        "type": "unknown"
      }
    ],
    "question_count": 6
  }
]
```

## Requirements
- Tesseract OCR installed
- Chinese language pack: `tesseract-ocr-chi-sim`
- Python packages: `pytesseract`, `PyMuPDF`, `Pillow`

## Installation
```bash
# Install Tesseract and Chinese support
sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim

# Install Python packages
pip install pytesseract PyMuPDF pillow
```

## Performance
- Speed: ~2-3 seconds per page
- Accuracy: Good for printed Chinese text
- No API costs or quotas
- Runs completely offline

## Tips
- OCR works best on clear, high-resolution scans
- Some mathematical symbols may need manual correction
- Question parsing uses simple pattern matching
- Review extracted questions for accuracy
