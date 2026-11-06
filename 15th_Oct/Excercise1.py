import pymupdf
pdf = pymupdf.open("EY_Digital_PDF_Practice.pdf")
print(pdf.page_count)
######################################
page_num = 0
page = pdf[page_num]
text = page.get_text()
print(text)
######################################
text = ""
for page in pdf:
    text += page.get_text()
print(text)
######################################

word = "maintenance"
for page_num in range(pdf.page_count):
    page = pdf[page_num]
    matches = page.search_for(word)

    if matches:
        print(word , f"found on page {page_num}")
    else:
        print(word , f"not found on page {page_num}")

#########################################################

word = "V303"
count = 0
for page_num in range(pdf.page_count):
    page = pdf[page_num]
    matches = page.search_for(word)

    if matches:
        count = count + 1

print(word , f" appears {count} times")

##########################################################

page_number = 1
page = pdf[page_number]
text = page.get_text()
print(text)

##################################################

with open("digital_pdf_text.txt", "w" , encoding="utf-8") as f:
    for page in pdf:
        f.write(page.get_text())
        f.write("\n\n")

#######################################################################3
