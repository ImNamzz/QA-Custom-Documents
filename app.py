import pymupdf as pf

path = r"E:\QA_Document\data\CV.pdf"

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

def pdf_tree(pdf_path, map_sizes_level):
    root = {"level": -1, "text": "ROOT", "children": []}    #create fake parent so stack could attached to
    path = [root]

    for page in pdf_path:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block and block.get("lines"):
                block_text = "".join(span["text"] for line in block["lines"] for span in line["spans"])
                primary_size = round(block["lines"][0]["spans"][0]["size"])
                level = map_sizes_level.get(primary_size, 99)
                node = {"level": level, "text": block_text.strip(), "children": []}

                while path[-1]["level"] >= level:
                    path.pop()

                path[-1]["children"].append(node)
                path.append(node)
    return root

def print_tree(node, indent=""):
    if node["level"] > -1:
        print(f"{indent}[L{node['level']}] {node['text']}")
    for child in node["children"]:
        print_tree(child, indent + "  ")

pdf_path = pf.open(path)
print("____Analyze Font Level____")
level_map = font_level(pdf_path)
print("Level Mapping Structure (Size -> Level): ")
for size, level in sorted(level_map.items(), key=lambda item: item[1]):
    print(f"  Level {level}: {size}pt")

document_tree = pdf_tree(pdf_path, level_map)
print("\n____Document Structure____")
print_tree(document_tree)

pdf_path.close()
# def extract_font_size(pdf_path):

#     doc = pf.open(pdf_path)
#     print(f"document'{pdf_path}' with {len(doc)} pages")
    
#     document_data = []
#     for page_num, page in enumerate(doc):
#         print(f"\n ___page {page_num}___ ")
#         blocks = page.get_text("dict")["blocks"]    
#         for block in blocks:
#             if "lines" in block:
#                 for line in block["lines"]:
#                     for span in line["spans"]:
#                         text = span["text"]
#                         font_name = span["font"]
#                         font_size = round(span["size"])
#                         print(f"font: {font_name}, size: {font_size}pt | text: '{text.strip()}'")
#     doc.close()
#     return document_data
#extract_font_size(pdf_path)

# version 1.0
# Rules:
# - I should treat larger font sizes as parents to smaller ones. In the end, the smallest will be the paragraph section.
# List could also be heading
# - Font styles could normally be used to emphasize, or sub titles
# - Should somehow treat header and footer properly, they could cause noise for chunks
# In this case, this shouldn't be treated like how normal pdf parser works anymore.
# Using tree might work.
# The tree should split headings -> subheadings -> ... -> text based on font sizes level mapped earlier
# In case the font size doesn't find a match (which it should not). assign it to level 99

