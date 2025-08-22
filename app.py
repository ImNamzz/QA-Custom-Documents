from pypdf import PdfReader

pdf_path = "E:\QA_Document\CV.pdf"

def read_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    texts = ""
    for page in reader.pages:
        texts += page.extract_text() or ""
        texts += "\n"
    return texts

reader = PdfReader(pdf_path)
print(str(reader.metadata))

print(read_pdf(pdf_path))
