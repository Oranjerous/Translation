
from docx import Document

def fill_residence_template(data, template_path, output_path):
    doc = Document(template_path)
    for p in doc.paragraphs:
        for r in p.runs:
            for key, val in data.items():
                placeholder = "{" + key + "}"
                if placeholder in r.text:
                    r.text = r.text.replace(placeholder, val)
    doc.save(output_path)
