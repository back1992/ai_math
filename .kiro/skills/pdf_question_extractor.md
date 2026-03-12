# PDF Question Extractor Skill

## Purpose
Extract math questions from educational PDF documents with progress tracking to avoid duplicate processing.

## Capabilities
- Convert PDF pages to images
- Track extraction progress (completed, in-progress, skipped, pending)
- Avoid duplicate processing
- Generate structured JSON output with bilingual content
- Resume from last checkpoint

## Usage

### Check Progress Status
```bash
python track_progress.py status
```

### Mark Pages as Completed
```bash
# Single page
python track_progress.py complete 11 "Extracted page 11"

# Multiple pages
python track_progress.py complete 11,12,13,14,15 "Batch 1 completed"
```

### Mark Pages as Skipped
```bash
python track_progress.py skip 1,2,3,4,5 "Introduction pages - no questions"
```

### Get Next Batch to Process
```bash
# Get next 10 pages
python track_progress.py next 10

# Get next 20 pages
python track_progress.py next 20
```

### Run Extraction with Auto-Tracking
```python
from extract_with_tracking import process_pdf_with_tracking

# Process next batch automatically (skips completed pages)
process_pdf_with_tracking(
    pdf_path='data/your_file.pdf',
    output_json='output/result.json'
)

# Process specific page range
process_pdf_with_tracking(
    pdf_path='data/your_file.pdf',
    output_json='output/result.json',
    start_page=21,
    end_page=30
)

# Force reprocess even if completed
process_pdf_with_tracking(
    pdf_path='data/your_file.pdf',
    output_json='output/result.json',
    start_page=11,
    end_page=20,
    force=True
)
```

## Project Structure
```
project/
├── data/                          # Input PDF files
├── output/
│   ├── images/                    # Converted page images
│   └── part01_zh_kp.json         # Extracted questions
├── progress.json                  # Progress tracking
├── track_progress.py              # Progress utilities
└── extract_with_tracking.py       # Main extraction script
```

## Progress Tracking Format

### progress.json Structure
```json
{
  "project": "ai_math_extraction",
  "total_pages": 90,
  "completed_pages": [11, 12, 13],
  "in_progress_pages": [],
  "skipped_pages": [1, 2, 3, 4, 5],
  "last_updated": "2026-03-12",
  "notes": {
    "pages_1_5": "Introduction/Cover pages",
    "pages_11_13": "Extracted successfully"
  }
}
```

## Output JSON Format

### Question Data Structure
```json
{
  "page": 11,
  "topic_en": "Inventions: Slinky",
  "topic_zh": "发明：弹簧玩具 (Slinky)",
  "context_en": "The Slinky was invented...",
  "context_zh": "弹簧玩具是由...",
  "clues_en": ["1) A >= 2 x 15", "..."],
  "clues_zh": ["1) A >= 2 x 15", "..."],
  "questions_en": ["1. What are all...", "..."],
  "questions_zh": ["1. 艾玛列表上的...", "..."],
  "knowledge_points": ["Algebraic Reasoning", "Factors"]
}
```

## Dependencies
```bash
pip install pdf2image pillow
```

### System Requirements
- `poppler-utils` (for pdf2image)
  - Ubuntu/Debian: `sudo apt-get install poppler-utils`
  - macOS: `brew install poppler`
  - Windows: Download from poppler releases

## Common Workflows

### Initial Setup
1. Place PDF in `data/` folder
2. Update `progress.json` with total pages
3. Mark intro/cover pages as skipped if needed

### Batch Processing
1. Check status: `python track_progress.py status`
2. Get next batch: `python track_progress.py next 10`
3. Run extraction: `python extract_with_tracking.py`
4. Verify output in `output/` folder
5. Repeat until all pages processed

### Resume After Interruption
The system automatically resumes from last checkpoint:
```python
# Just run again - it skips completed pages
process_pdf_with_tracking(pdf_path, output_json)
```

### Manual Progress Update
If you extracted pages outside the tracking system:
```bash
# Mark them as completed to sync progress
python track_progress.py complete 21,22,23,24,25 "Manually extracted"
```

## Integration with Colab

### Sync Progress to Colab
```python
# In Colab notebook
from google.colab import drive
drive.mount('/content/drive')

# Copy progress file
!cp /content/drive/MyDrive/project/progress.json ./progress.json

# Load and check
from track_progress import show_status
show_status()
```

### Sync Progress from Colab
```python
# After processing in Colab
!cp ./progress.json /content/drive/MyDrive/project/progress.json
```

## Best Practices

1. **Always check status before processing**
   ```bash
   python track_progress.py status
   ```

2. **Process in small batches** (10-20 pages)
   - Easier to verify quality
   - Less data loss if interrupted

3. **Add notes for special cases**
   ```bash
   python track_progress.py skip 50,51 "Blank pages"
   ```

4. **Backup progress.json regularly**
   ```bash
   cp progress.json progress.backup.json
   ```

5. **Verify output after each batch**
   - Check JSON structure
   - Validate bilingual content
   - Review knowledge points

## Troubleshooting

### Pages marked as completed but not in output
```python
# Reprocess with force flag
process_pdf_with_tracking(pdf_path, output_json, start_page=X, end_page=Y, force=True)
```

### Reset progress for specific pages
```python
from track_progress import load_progress, save_progress

progress = load_progress()
# Remove from completed list
progress['completed_pages'] = [p for p in progress['completed_pages'] if p not in [21, 22, 23]]
save_progress(progress)
```

### Check for missing pages
```python
from track_progress import get_pending_pages
pending = get_pending_pages()
print(f"Missing pages: {pending}")
```

## Advanced Features

### Custom Batch Processing
```python
# Process only odd pages
for page in range(1, 91, 2):
    if not is_page_completed(page):
        process_pdf_with_tracking(pdf_path, output_json, page, page)
```

### Parallel Processing
```python
# Process multiple ranges in parallel (use with caution)
from multiprocessing import Process

def process_range(start, end):
    process_pdf_with_tracking(pdf_path, output_json, start, end)

p1 = Process(target=process_range, args=(21, 30))
p2 = Process(target=process_range, args=(31, 40))
p1.start()
p2.start()
```

## Notes
- Progress tracking is local to the project directory
- Output JSON is automatically merged (no duplicates)
- Images are saved to `output/images/` for reference
- All text uses UTF-8 encoding for multilingual support
