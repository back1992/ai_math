# Code Design Plan: AI Math Question Extractor

## Project Overview
Extract math questions from educational PDF documents and convert them into structured JSON format for AI model fine-tuning.

## Current Architecture

### Data Flow
```
PDF Document → Image Conversion → Question Extraction → JSON Output
                                         ↓
                                   Firebase Firestore
                                   (Ground Truth Storage)
```

### Existing Components

1. **PDF to Image Converter** (`convert_pdf.py`)
   - Converts PDF pages to JPEG images
   - Uses `pdf2image` library
   - Saves to `output/images/`

2. **Colab Notebook** (`ai_math.ipynb`)
   - Main processing pipeline
   - Firebase integration for ground truth data
   - Generates training data in JSONL format

3. **Output Structure** (`output/part01_zh_kp.json`)
   - Bilingual (English/Chinese) question data
   - Structured format with topics, context, clues, questions, knowledge points

## Design Goals

### 1. Modular Architecture
Separate concerns into independent, reusable modules:

```
src/
├── pdf_processor.py      # PDF to image conversion
├── question_extractor.py # Extract questions from images/text
├── data_validator.py     # Validate extracted data structure
├── firebase_client.py    # Firebase operations (optional)
└── output_formatter.py   # Format and save JSON output
```

### 2. Data Model

```python
class Question:
    page: int
    topic_en: str
    topic_zh: str
    context_en: str
    context_zh: str
    clues_en: List[str]
    clues_zh: List[str]
    questions_en: List[str]
    questions_zh: List[str]
    knowledge_points: List[str]
```

### 3. Processing Pipeline

#### Stage 1: PDF Processing
```python
def process_pdf(pdf_path, start_page, end_page):
    """
    Convert PDF pages to images
    Returns: List of (page_num, image_path) tuples
    """
    - Load PDF
    - Convert specified page range to images
    - Save images to output/images/
    - Return image paths
```

#### Stage 2: Question Extraction
```python
def extract_questions(image_path, page_num):
    """
    Extract structured question data from page image
    Returns: Question object
    """
    - OCR or vision model to read text
    - Parse structure (topic, context, clues, questions)
    - Identify knowledge points
    - Return structured data
```

#### Stage 3: Validation
```python
def validate_question(question_data):
    """
    Validate extracted data meets schema requirements
    Returns: (is_valid, errors)
    """
    - Check required fields present
    - Verify data types
    - Validate bilingual pairs match
    - Return validation result
```

#### Stage 4: Output Generation
```python
def save_to_json(questions, output_path):
    """
    Save validated questions to JSON file
    """
    - Format as JSON array
    - Ensure UTF-8 encoding
    - Pretty print with indentation
    - Save to output path
```

## Implementation Strategy

### Phase 1: Refactor Existing Code (Week 1)
- Extract reusable functions from notebook
- Create modular Python scripts
- Add error handling and logging
- Write unit tests for each module

### Phase 2: Improve Extraction Logic (Week 2)
- Implement OCR or vision API integration
- Add pattern matching for question structures
- Handle edge cases (multi-column, images, formulas)
- Support batch processing

### Phase 3: Firebase Integration (Week 3)
- Separate Firebase logic into dedicated module
- Add offline mode (work without Firebase)
- Implement sync mechanism
- Add ground truth comparison

### Phase 4: Automation & Testing (Week 4)
- Create CLI interface
- Add progress tracking
- Implement resume capability
- Full integration testing

## Technology Stack

### Core Dependencies
- `pdf2image`: PDF to image conversion
- `Pillow`: Image processing
- `firebase-admin`: Firebase integration (optional)

### Potential Additions
- `pytesseract`: OCR for text extraction
- `opencv-python`: Advanced image processing
- `pydantic`: Data validation
- `click`: CLI interface
- `pytest`: Testing framework

## Configuration Management

### config.yaml
```yaml
pdf:
  input_path: "data/"
  output_images: "output/images/"
  dpi: 300

extraction:
  start_page: 1
  end_page: 90
  batch_size: 10

output:
  format: "json"
  path: "output/"
  encoding: "utf-8"

firebase:
  enabled: false
  credentials_path: ""
  collection: "extracted_questions"
```

## Error Handling Strategy

1. **PDF Processing Errors**
   - Invalid PDF format
   - Missing pages
   - Conversion failures

2. **Extraction Errors**
   - Unreadable text
   - Unexpected page structure
   - Missing bilingual content

3. **Validation Errors**
   - Schema violations
   - Missing required fields
   - Data type mismatches

4. **Output Errors**
   - File write permissions
   - Disk space issues
   - Encoding problems

## Testing Strategy

### Unit Tests
- Test each module independently
- Mock external dependencies
- Cover edge cases

### Integration Tests
- Test full pipeline end-to-end
- Use sample PDF pages
- Verify output format

### Validation Tests
- Compare against ground truth
- Check bilingual consistency
- Verify knowledge point accuracy

## Deployment Options

### Option 1: Local Development (Kiro)
- Full IDE features
- Version control with Git
- Local testing and debugging

### Option 2: Cloud Execution (Colab)
- Free GPU/TPU access
- Firebase integration
- Collaborative environment

### Option 3: Hybrid Approach (Recommended)
- Develop and edit in Kiro
- Push to GitHub
- Execute in Colab for heavy processing
- Pull results back to local

## Future Enhancements

1. **AI-Powered Extraction**
   - Use vision-language models (GPT-4V, Gemini)
   - Automatic translation
   - Knowledge point classification

2. **Quality Assurance**
   - Human-in-the-loop review interface
   - Confidence scoring
   - Automated correction suggestions

3. **Scalability**
   - Parallel processing
   - Cloud storage integration
   - API service deployment

4. **Analytics**
   - Extraction success rate
   - Processing time metrics
   - Quality score tracking

## Success Metrics

- Extract all 90 pages successfully
- 95%+ accuracy vs ground truth
- Process 10 pages per minute
- Zero data loss or corruption
- Bilingual content 100% aligned

## Timeline

- Week 1: Modular refactoring
- Week 2: Enhanced extraction
- Week 3: Firebase integration
- Week 4: Testing & automation
- Week 5+: AI-powered improvements

## Next Steps

1. Review and approve this design plan
2. Set up project structure (`src/` directory)
3. Begin Phase 1 refactoring
4. Create development branch in Git
5. Implement first module with tests
