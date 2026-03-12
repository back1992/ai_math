# Project Review: ai_math

## Overview
The `ai_math` project is a specialized utility designed to automate the creation of a fine-tuning dataset for AI models. Its primary objective is to enable models to accurately extract and format math questions from educational PDF documents into structured JSON data.

## Key Components

### 1. Data Processing Pipeline (`ai_math.ipynb`)
The project utilizes a Jupyter Notebook (optimized for Google Colab) to handle the end-to-end data preparation workflow:
- **PDF to Image Conversion**: Uses `pdf2image` and `poppler-utils` to transform PDF pages into high-quality JPEG images.
- **Ground Truth Integration**: Interfaces with Google Firestore to retrieve manually verified or "perfect" JSON representations of math questions for each page.
- **Dataset Formatting**: Aggregates images and their corresponding JSON responses into a `.jsonl` format, which is standard for fine-tuning large language or multi-modal models.

### 2. Logic & Rules
- **Page Classification**: The system includes logic to automatically flag the first 5 pages of a document as "Introduction/Cover" pages, providing a negative training signal (empty question sets) to the model.
- **Instructional Prompting**: Each dataset entry is prefixed with a consistent instruction: *"Extract all math questions from this page and format as JSON."*

### 3. Source Materials
- **Target Document**: `data/Algebra Readiness Made Easy Grade 6...pdf` serves as the primary source for training data.
- **Infrastructure**: Dependencies include `firebase-admin` for data retrieval and `pdf2image` for vision-based processing.

## Current Project Status
- **Implementation**: The core conversion and alignment logic is fully implemented in the notebook.
- **Data Gap**: Based on the latest execution logs, only the first 5 pages have been successfully aligned. Pages 6 through 90 are currently missing their corresponding entries in Firestore, indicating that the manual "ground truth" extraction phase is still in progress.
- **Environment**: The project is heavily coupled with Google Colab and Google Drive paths (`/content/drive/MyDrive/...`), which may require adjustment for local or containerized execution.

## Recommendations
1. **Local Portability**: Update the notebook or create a Python script to use relative paths (e.g., `./data/`) instead of hardcoded Google Drive paths to improve portability across different environments.
2. **Data Completion**: Prioritize the extraction and upload of the remaining 85 pages of math questions to Firestore to complete the training dataset.
3. **Environment Configuration**: Add a `requirements.txt` file to the root directory to simplify dependency management for non-Colab users.
4. **Documentation**: Expand the root `README.md` to include setup instructions and a description of the Firestore schema required for the `extracted_questions` collection.
