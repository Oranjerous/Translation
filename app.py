
from flask import Flask, render_template, request, send_file
import os
from PIL import Image
import pytesseract
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

@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        files = request.files.getlist("images")
        output_paths = []

        for file in files:
            filename = secure_filename(file.filename)
            path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_{filename}")
            file.save(path)

            # مؤقتًا - بيانات تجريبية لحين تنفيذ OCR دقيق
            data = {
                "PERSON_NO": "123456789",
                "NAME": "Test Name",
                "NATIONALITY": "Jordanian",
                "DOB": "1990-01-01",
                "PASSPORT_NO": "A1234567",
                "RESIDENCE_NO": "1234567890",
                "ISSUE_DATE": "2024-01-01",
                "EXPIRY_DATE": "2029-01-01",
                "PROFESSION": "Engineer",
                "ADDRESS": "Amman, Jordan",
                "POLICE_STATION": "Residence Department",
                "CARD_NO": "987654"
            }

            output_file = os.path.join(GENERATED_FOLDER, f"{uuid.uuid4()}.docx")
            fill_residence_template(data, TEMPLATE_PATH, output_file)
            output_paths.append(output_file)

        return send_file(output_paths[0], as_attachment=True)

    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)
