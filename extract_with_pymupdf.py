"""
Enhanced PDF extraction using PyMuPDF with progress tracking
"""
import fitz  # PyMuPDF
import json
import os
from track_progress import (
    load_progress, 
    mark_completed, 
    mark_in_progress,
    is_page_completed,
    get_next_batch,
    show_status
)

def extract_page_to_image(pdf_path, page_num, output_folder='output/images', zoom=2):
    """
    Extract a PDF page as high-quality image
    
    Args:
        pdf_path: Path to PDF file
        page_num: Page number (1-indexed)
        output_folder: Where to save images
        zoom: Quality multiplier (2 = 2x resolution)
    
    Returns:
        Path to saved image
    """
    doc = fitz.open(pdf_path)
    page = doc[page_num - 1]  # Convert to 0-indexed
    
    # Render page to image
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    
    # Save image
    img_path = os.path.join(output_folder, f'page_{page_num}.jpg')
    pix.save(img_path)
    
    doc.close()
    return img_path

def extract_page_text(pdf_path, page_num):
    """
    Extract text from a PDF page
    
    Args:
        pdf_path: Path to PDF file
        page_num: Page number (1-indexed)
    
    Returns:
        Extracted text string
    """
    doc = fitz.open(pdf_path)
    page = doc[page_num - 1]
    text = page.get_text()
    doc.close()
    return text

def get_pdf_info(pdf_path):
    """Get PDF metadata"""
    doc = fitz.open(pdf_path)
    info = {
        'page_count': len(doc),
        'metadata': doc.metadata
    }
    doc.close()
    return info

def process_pages_batch(pdf_path, output_json, pages_to_process, force=False):
    """
    Process a batch of pages with progress tracking
    
    Args:
        pdf_path: Path to PDF file
        output_json: Output JSON file
        pages_to_process: List of page numbers to process
        force: Reprocess even if completed
    """
    output_folder = 'output/images'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Filter completed pages
    if not force:
        pages_to_process = [p for p in pages_to_process if not is_page_completed(p)]
        if not pages_to_process:
            print("✅ All pages in batch already completed!")
            return
    
    print(f"\n🚀 Processing {len(pages_to_process)} pages: {pages_to_process}")
    mark_in_progress(pages_to_process)
    
    # Load existing results
    if os.path.exists(output_json):
        with open(output_json, 'r', encoding='utf-8') as f:
            results = json.load(f)
    else:
        results = []
    
    newly_extracted = []
    
    for page_num in pages_to_process:
        print(f"\n📄 Processing page {page_num}...")
        
        # Extract image
        img_path = extract_page_to_image(pdf_path, page_num, output_folder)
        print(f"  ✅ Image saved: {img_path}")
        
        # Extract text
        text = extract_page_text(pdf_path, page_num)
        print(f"  ✅ Text extracted: {len(text)} characters")
        
        # TODO: Parse text into structured format
        # For now, create template structure
        question_data = {
            "page": page_num,
            "raw_text": text[:500],  # First 500 chars for reference
            "image_path": img_path,
            "topic_en": "",
            "topic_zh": "",
            "context_en": "",
            "context_zh": "",
            "clues_en": [],
            "clues_zh": [],
            "questions_en": [],
            "questions_zh": [],
            "knowledge_points": []
        }
        
        newly_extracted.append(question_data)
        mark_completed(page_num)
        print(f"  ✅ Page {page_num} completed")
    
    # Merge with existing results
    existing_pages = {item['page'] for item in results}
    for item in newly_extracted:
        if item['page'] not in existing_pages:
            results.append(item)
        else:
            # Update existing entry
            results = [item if r['page'] == item['page'] else r for r in results]
    
    # Sort by page number
    results.sort(key=lambda x: x['page'])
    
    # Save to JSON
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Saved {len(newly_extracted)} pages to {output_json}")
    print(f"📊 Total pages in output: {len(results)}")

def main():
    """Main execution"""
    pdf_path = 'data/Algebra Readiness Made Easy Grade 6_ An Essential Part of Every Math Curriculum_Mary Cavanagh, Carol Findell, Carole Greenes.pdf'
    output_json = 'output/extracted_pages.json'
    
    # Show status
    show_status()
    
    # Get next batch
    next_batch = get_next_batch(10)
    
    if not next_batch:
        print("\n✅ All pages completed!")
        return
    
    print(f"\n🔜 Next batch: {next_batch}")
    
    # Process batch
    process_pages_batch(pdf_path, output_json, next_batch)
    
    # Show updated status
    show_status()

if __name__ == "__main__":
    main()
