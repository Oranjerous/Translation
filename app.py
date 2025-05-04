from flask import Flask, render_template, request, send_file
import os
from PIL import Image
from paddleocr import PaddleOCR
from docx import Document
from fill_template import fill_residence_template
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
GENERATED_FOLDER = "static/generated"
TEMPLATE_PATH = "static/Residence_Template_Fillable.docx"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)

ocr = PaddleOCR(use_angle_cls=True, lang='ar')

def extract_data_from_image(image_path):
    result = ocr.ocr(image_path, cls=True)
    extracted_text = "\n".join([line[1][0] for line in result[0]])

    data = {
        "PERSON_NO": "",
        "NAME": "",
        "NATIONALITY": "",
        "DOB": "",
        "PASSPORT_NO": "",
        "RESIDENCE_NO": "",
        "ISSUE_DATE": "",
        "EXPIRY_DATE": "",
        "PROFESSION": "",
        "ADDRESS": "",
        "POLICE_STATION": "",
        "CARD_NO": ""
    }

    lines = extracted_text.splitlines()
    for line in lines:
        if "Name" in line or "الاسم" in line:
            data["NAME"] = line.split(":")[-1].strip()
        if "Nationality" in line or "الجنسية" in line:
            data["NATIONALITY"] = line.split(":")[-1].strip()
        if "Passport" in line:
            data["PASSPORT_NO"] = line.split(":")[-1].strip()
        if "Profession" in line or "المهنة" in line:
            data["PROFESSION"] = line.split(":")[-1].strip()
        if "Address" in line or "العنوان" in line:
            data["ADDRESS"] = line.split(":")[-1].strip()
        if "Date of Birth" in line or "تاريخ الميلاد" in line:
            data["DOB"] = line.split(":")[-1].strip()
        if "Issue Date" in line or "تاريخ الاصدار" in line:
            data["ISSUE_DATE"] = line.split(":")[-1].strip()
        if "Expiry Date" in line or "تاريخ الانتهاء" in line:
            data["EXPIRY_DATE"] = line.split(":")[-1].strip()
        if "Card" in line or "البطاقة" in line:
            data["CARD_NO"] = ''.join(filter(str.isdigit, line))

    return data

@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        files = request.files.getlist("images")
        output_paths = []

        for file in files:
            filename = secure_filename(file.filename)
            path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_{filename}")
            file.save(path)

            extracted_data = extract_data_from_image(path)

            output_file = os.path.join(GENERATED_FOLDER, f"{uuid.uuid4()}.docx")
            fill_residence_template(extracted_data, TEMPLATE_PATH, output_file)
            output_paths.append(output_file)

        return send_file(output_paths[0], as_attachment=True)

    return render_template("upload.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)