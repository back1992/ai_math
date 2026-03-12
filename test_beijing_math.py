"""
Test extraction for Beijing Math exam PDF
"""
import fitz
import os

pdf_path = 'data/北京各区分班考试真题集—数学 .pdf'
output_folder = 'output/beijing_math_images'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

doc = fitz.open(pdf_path)

print(f"📚 PDF Info:")
print(f"  Total pages: {len(doc)}")
print(f"  Title: {doc.metadata.get('title', 'N/A')}")

# Extract first 10 pages as samples
print(f"\n🖼️  Extracting sample pages...")
for page_num in range(1, 11):
    page = doc[page_num - 1]
    mat = fitz.Matrix(2, 2)
    pix = page.get_pixmap(matrix=mat)
    img_path = f"{output_folder}/page_{page_num}.jpg"
    pix.save(img_path)
    print(f"  ✅ Page {page_num}: {pix.width}x{pix.height}")

doc.close()

print(f"\n✅ Saved to {output_folder}/")
print(f"\n💡 Next steps:")
print(f"  1. Check the images to see question structure")
print(f"  2. Use Gemini/OCR to extract Chinese text")
print(f"  3. Parse into structured format")
