from flask import Flask, request, send_file
from pdf2docx import Converter
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
CONVERTED_FOLDER = 'converted'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

@app.route('/convert', methods=['POST'])
def convert_pdf_to_word():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    upload_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(upload_path)

    output_filename = os.path.splitext(file.filename)[0] + '.docx'
    output_path = os.path.join(CONVERTED_FOLDER, output_filename)

    cv = Converter(upload_path)
    cv.convert(output_path, start=0, end=None)
    cv.close()

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)