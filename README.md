# ai_math

`ai_math` is a dataset preparation tool designed to facilitate the fine-tuning of AI models for math question extraction from PDFs. It converts PDF pages into images and aligns them with ground truth JSON data fetched from Firestore to create a standard `.jsonl` fine-tuning dataset.

## Features
- **PDF-to-Image Conversion**: Batch process PDF pages into JPEG images.
- **Data Alignment**: Automatically syncs images with "perfect" JSON extraction results stored in Google Firestore.
- **Fine-Tuning Ready**: Generates training-ready `.jsonl` files compatible with most AI fine-tuning platforms.
- **Automated Filtering**: Includes logic to identify and label non-question pages (e.g., covers, intro).

## Project Structure
- `ai_math.ipynb`: Core processing logic (optimized for Google Colab).
- `data/`: Contains source PDF documents for extraction.
- `docs/`: Project documentation and reviews.
- `.venv/`: Local Python virtual environment.

## Setup & Usage
1. **Dependencies**:
   - `poppler-utils` (system package)
   - `pdf2image`
   - `firebase-admin`
2. **Environment**:
   - Designed for execution in Google Colab with access to Google Drive and Firestore.
   - Requires a `serviceAccountKey.json` for Firebase authentication.
3. **Execution**: Run the cells in `ai_math.ipynb` to process PDFs and generate the dataset.

## Documentation
For a detailed analysis of the project, see [docs/project_review.md](docs/project_review.md).
