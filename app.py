import pymupdf as pf

pdf_path = "E:\QA_Document\data\CV.pdf"

def extract_font_size(pdf_path):

    doc = pf.open(pdf_path)
    print(f"document'{pdf_path}' with {len(doc)} pages")
    
    document_data = []
    for page_num, page in enumerate(doc):
        print(f"\n ___page {page_num}___ ")
        blocks = page.get_text("dict")["blocks"]    
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"]
                        font_name = span["font"]
                        font_size = round(span["size"])
                        print(f"font: {font_name}, size: {font_size}pt | text: '{text.strip()}'")
    doc.close()
    return document_data

extract_font_size(pdf_path)