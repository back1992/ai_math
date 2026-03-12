import os
from pdf2image import convert_from_path

pdf_path = 'data/Algebra Readiness Made Easy Grade 6_ An Essential Part of Every Math Curriculum_Mary Cavanagh, Carol Findell, Carole Greenes.pdf'
output_folder = 'output/images'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Convert first 10 pages for initial extraction
pages = convert_from_path(pdf_path, first_page=1, last_page=10)

for i, page in enumerate(pages):
    page_num = i + 1
    img_name = f"page_{page_num}.jpg"
    img_path = os.path.join(output_folder, img_name)
    page.save(img_path, 'JPEG')
    print(f"Saved {img_path}")
