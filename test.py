import fitz
import time

with fitz.open(r"C:\Users\uglycat\Documents\playnplay-screen\pdfs\2022-10-19 12_47_07.535848.pdf") as doc:
    for page in doc:
        text = page.get_text()
        time.sleep(5)
        print(text)