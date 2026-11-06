import pymupdf
pdf = pymupdf.open("EY_Scanned_PDF_OCR_Practice.pdf")
for page_num in range(pdf.page_count):
    page = pdf[page_num]

    pix = page.get_pixmap()
    pix.save(f"page_{page_num+1}.png")

#############################################################

print(pytesseract.image_to_string(Image.open("page1.png")))

#############################################################
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

img = Image.open("page_1.png")

text = pytesseract.image_to_string(img)

print(text)

#############################################################


if "Forklift FL-17" in text:
    print("Forklift FL-17 was detected.")
else:
    print("Forklift FL-17 was not detected.")

#############################################################

if "injuries" in text:
    print("Word was detected.")
else:
    print("Word was not detected.")

#############################################################

for line in text.splitlines():
    if "inspection" in line:
        print(line)

#############################################################

with open("ocr_result.txt", "w" , encoding="utf-8") as f:
    f.write(text)

#############################################################

count = 0
for line in text.splitlines():
    if "inspection" in line:
        count += 1

print(count)

##################################################################

for line in text.splitlines():
    if "Loading Bay" in line:
        print(line)
        
#################################################################
