"""
Complete Beijing Math extraction pipeline using free OCR
No API limits, runs locally
"""
import fitz
import json
import os
from PIL import Image
import pytesseract
import re

def extract_page_with_ocr(pdf_path, page_num):
    """Extract text from PDF page using OCR"""
    doc = fitz.open(pdf_path)
    page = doc[page_num - 1]
    mat = fitz.Matrix(2, 2)
    pix = page.get_pixmap(matrix=mat)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    text = pytesseract.image_to_string(img, lang='chi_sim')
    doc.close()
    return text

def parse_questions_from_text(text, page_num):
    """
    Parse questions from OCR text
    Simple pattern matching for numbered questions
    """
    questions = []
    
    # Pattern for questions: number followed by period or parenthesis
    # e.g., "1. ", "1、", "（1）"
    lines = text.split('\n')
    current_question = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check if line starts with question number
        match = re.match(r'^(\d+)[.、．）\)]\s*(.+)', line)
        if match:
            # Save previous question
            if current_question:
                questions.append(current_question)
            
            # Start new question
            num = match.group(1)
            content = match.group(2)
            current_question = {
                "number": num,
                "content": content,
                "type": "unknown"
            }
        elif current_question:
            # Continue previous question
            current_question["content"] += " " + line
    
    # Add last question
    if current_question:
        questions.append(current_question)
    
    return {
        "page": page_num,
        "raw_text": text,
        "questions": questions,
        "question_count": len(questions)
    }

def extract_all_pages(pdf_path, start_page, end_page, output_json):
    """Extract all pages with progress tracking"""
    results = []
    
    print(f"🚀 Extracting pages {start_page}-{end_page} from Beijing Math PDF")
    print(f"📝 Using free Tesseract OCR (no API limits)\n")
    
    for page_num in range(start_page, end_page + 1):
        print(f"📄 Page {page_num}...", end=" ")
        
        try:
            # OCR extraction
            text = extract_page_with_ocr(pdf_path, page_num)
            
            # Parse questions
            parsed = parse_questions_from_text(text, page_num)
            results.append(parsed)
            
            print(f"✅ {parsed['question_count']} questions, {len(text)} chars")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Save results
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    total_questions = sum(r['question_count'] for r in results)
    print(f"\n✅ Complete!")
    print(f"📊 Extracted {len(results)} pages, {total_questions} questions")
    print(f"💾 Saved to {output_json}")
    
    return results

if __name__ == "__main__":
    pdf_path = 'data/北京各区分班考试真题集—数学 .pdf'
    output_json = 'output/beijing_math_questions.json'
    
    # Extract pages 5-20 as test (skip cover pages 1-4)
    results = extract_all_pages(pdf_path, 5, 20, output_json)
    
    # Show sample
    if results and results[0]['questions']:
        print(f"\n📄 Sample question from page {results[0]['page']}:")
        q = results[0]['questions'][0]
        print(f"  {q['number']}. {q['content'][:100]}...")
