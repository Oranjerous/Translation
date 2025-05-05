
from flask import Flask, request, send_file, render_template
from paddleocr import PaddleOCR
from docx import Document
import os
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)
ocr = PaddleOCR(use_angle_cls=True, lang='ar')

UPLOAD_FOLDER = "uploads"
TEMPLATE_PATH = "Residence_Template_Fillable.docx"
OUTPUT_PATH = "translated_output.docx"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# مواضع الحقول داخل كل صورة
REGIONS = {
    "passport": {
        "name": (150, 385, 750, 425)  # الاسم من الجواز
    },
    "front": {
        "residence": (500, 470, 1100, 510),
        "passport": (500, 420, 1100, 460),
        "dob": (500, 320, 1100, 360),
        "nationality": (500, 270, 1100, 310),
        "issue": (500, 520, 1100, 560),
        "expiry": (500, 570, 1100, 610)
    },
    "back": {
        "profession": (150, 20, 1150, 60),
        "address": (150, 60, 1150, 100),
        "police": (150, 100, 1150, 140)
    }
}

def extract_fields_by_regions(image_paths):
    data = {}
    for key, image_path in image_paths.items():
        image = Image.open(image_path).convert('RGB')
        regions = REGIONS.get(key, {})
        for field, box in regions.items():
            cropped = image.crop(box)
            cropped_path = os.path.join(UPLOAD_FOLDER, f"{field}.jpg")
            cropped.save(cropped_path)

            result = ocr.ocr(cropped_path)[0]
            text = ""
            for line in result:
                text += line[1][0] + " "
            data[field] = text.strip()
    return data

@app.route('/', methods=['GET', 'POST'])
def upload_images():
    if request.method == 'POST':
        files = request.files
        image_paths = {}
        for field in ["passport", "front", "back"]:
            f = files.get(field)
            if f:
                filename = secure_filename(f.filename)
                path = os.path.join(UPLOAD_FOLDER, filename)
                f.save(path)
                image_paths[field] = path

        extracted_data = extract_fields_by_regions(image_paths)
        fill_template(extracted_data, TEMPLATE_PATH, OUTPUT_PATH)
        return send_file(OUTPUT_PATH, as_attachment=True)

    return render_template('upload_multi.html')

def fill_template(data, template_path, output_path):
    doc = Document(template_path)
    for para in doc.paragraphs:
        if "Name:" in para.text:
            para.text = f"Name: {data.get('name', '')}"
        elif "Passport No:" in para.text:
            para.text = f"Passport No: {data.get('passport', '')}"
        elif "Residence No:" in para.text:
            para.text = f"Residence No: {data.get('residence', '')}"
        elif "Issue Date:" in para.text:
            para.text = f"Issue Date: {data.get('issue', '')}"
        elif "Expiry Date:" in para.text:
            para.text = f"Expiry Date: {data.get('expiry', '')}"
        elif "Profession:" in para.text:
            para.text = f"Profession: {data.get('profession', '')}"
        elif "Address:" in para.text:
            para.text = f"Address: {data.get('address', '')}"
        elif "Police Station:" in para.text:
            para.text = f"Police Station: {data.get('police', '')}"
        elif "Date Of Birth:" in para.text:
            para.text = f"Date Of Birth: {data.get('dob', '')}"
        elif "Nationality:" in para.text:
            para.text = f"Nationality: {data.get('nationality', '')}"
    doc.save(output_path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
