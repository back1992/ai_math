"""
Extract ALL pages from Beijing Math PDF (5-256)
Uses free OCR, no API limits
"""
from extract_beijing_complete import extract_all_pages

pdf_path = 'data/北京各区分班考试真题集—数学 .pdf'
output_json = 'output/beijing_math_all_questions.json'

print("🚀 Starting full extraction of Beijing Math PDF")
print("📚 Pages: 5-256 (252 pages)")
print("⏱️  Estimated time: ~10-15 minutes")
print("💰 Cost: FREE (using local OCR)\n")

# Extract all pages
results = extract_all_pages(pdf_path, 5, 256, output_json)

print("\n" + "="*60)
print("✅ EXTRACTION COMPLETE!")
print("="*60)
print(f"📄 Pages processed: {len(results)}")
print(f"❓ Total questions: {sum(r['question_count'] for r in results)}")
print(f"💾 Output: {output_json}")
