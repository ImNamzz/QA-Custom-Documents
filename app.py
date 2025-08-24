import pymupdf as pf

pdf_path = r"E:\QA_Document\data\CV.pdf"

def font_level(pdf_path):
    doc = pf.open(pdf_path)
    font_sizes = set()
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        font_sizes.add(round(span["size"]))
    doc.close()
    #sort the font size descending
    sort_sizes = sorted(list(font_sizes), reverse=True)
    #map each font size to it's corresponding level
    map_sizes_level = {}
    for i, size in enumerate(sort_sizes):
        map_sizes_level[size] = i

    return map_sizes_level


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
print(font_level(pdf_path))

# version 1.0
# Rules:
# - I should treat larger font sizes as parents to smaller ones. In the end, the smallest will be the paragraph section.
# List could also be heading
# - Font styles could normally be used to emphasize, or sub titles
# - Should somehow treat header and footer properly, they could cause noise for chunks
# In this case, this shouldn't be treated like how normal pdf parser works anymore.
# Using tree might work.
