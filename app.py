import os
from flask import Flask, render_template, request, send_file, after_this_request
from pdf2docx import Converter

app = Flask(__name__)
UPLOAD_FOLDER = 'conversions'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'pdf_file' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['pdf_file']
    if file.filename == '':
        return "No file selected", 400

    # Define paths
    pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
    docx_name = os.path.splitext(file.filename)[0] + ".docx"
    docx_path = os.path.join(UPLOAD_FOLDER, docx_name)
    
    file.save(pdf_path)

    try:
        # High-accuracy conversion settings
        # Replace your current cv.convert line with this improved version:
try:
    cv = Converter(pdf_path)
    
    # These settings force the engine to 'guess' spaces more aggressively
    cv.convert(docx_path, 
               start=0, 
               end=None, 
               ocr=1,             # Use OCR if text is missing
               force_ocr=True,    # Force OCR to re-examine word spacing
               connected_components=True) # Helps separate merged letters
    cv.close()

        @after_this_request
        def cleanup(response):
            try:
                os.remove(pdf_path)
            except Exception as e:
                print(f"Cleanup error: {e}")
            return response

        return send_file(docx_path, as_attachment=True)

    except Exception as e:
        return f"Conversion failed: {str(e)}", 500

if __name__ == '__main__':

    app.run(debug=True)
