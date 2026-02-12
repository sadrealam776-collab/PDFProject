import os
import time
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

# Absolute paths to avoid "File Not Found" errors
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'conversions')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'pdf_file' not in request.files:
        return "No file part", 400
    
    file = request.files['pdf_file']
    if file.filename == '':
        return "No selected file", 400

    # Create unique filename using timestamp to avoid "File in use" errors
    timestamp = int(time.time())
    pdf_path = os.path.join(UPLOAD_FOLDER, f"input_{timestamp}.pdf")
    docx_name = f"Converted_{timestamp}.docx"
    docx_path = os.path.join(UPLOAD_FOLDER, docx_name)
    
    file.save(pdf_path)

    try:
        from pdf2docx import Converter
        cv = Converter(pdf_path)
        # Advanced spacing and OCR settings for your resume
        cv.convert(docx_path, start=0, end=None, ocr=1, multi_processing=True)
        cv.close()

        # Clean up the input PDF immediately
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

        # Force the browser to treat this as a download
        return send_from_directory(
            UPLOAD_FOLDER, 
            docx_name, 
            as_attachment=True,
            download_name="Your_Converted_Resume.docx"
        )

    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
