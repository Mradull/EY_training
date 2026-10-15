from pypdf import PdfReader
reader = PdfReader('EY_Digital_PDF_Practice.pdf')
print(len(reader.pages))
######################################################
page = reader.pages[0]
text = page.extract_text()
print(text)
#######################################################
page = reader.pages[1]
text = page.extract_text()
print(text)
######################################################

text = reader.pages[0].extract_text() + reader.pages[1].extract_text()
print(text)
##################################################################
text = ""
for page in reader.pages:
    text += page.extract_text()
word = "NorthStar Maintenance"
if word in text:
    print(f"{word} found")
else:
    print(f"'{word} not found")
##################################################################
text = ""
count = 0
for page in reader.pages:
    text += page.extract_text()
    word = "vendor"
    if word in text:
        count = count+1
print(count)

##################################################################
text = ""
for page in reader.pages:
    text+= page.extract_text() +"\n"
with open("pypdf_output.txt","w" , encoding="utf-8") as f:
    f.write(text)
##################################################################
