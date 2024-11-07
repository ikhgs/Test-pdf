from flask import Flask, request, jsonify, send_from_directory
import fitz  # PyMuPDF
import os

app = Flask(__name__)

# Chemin vers le répertoire où les fichiers PDF sont stockés
PDF_FOLDER = 'pdf_files'

# Route pour téléverser et extraire le texte d'un fichier PDF
@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'pdf_file' not in request.files:
        return jsonify({"error": "Aucun fichier PDF trouvé"}), 400
    
    pdf_file = request.files['pdf_file']
    pdf_path = os.path.join(PDF_FOLDER, pdf_file.filename)
    pdf_file.save(pdf_path)
    
    text_content = extract_text_from_pdf(pdf_path)
    return jsonify({"text": text_content})

# Route pour obtenir le texte d'un PDF existant
@app.route('/get_pdf_text', methods=['GET'])
def get_pdf_text():
    pdf_name = request.args.get('filename')
    if not pdf_name:
        return jsonify({"error": "Aucun nom de fichier spécifié"}), 400
    
    pdf_path = os.path.join(PDF_FOLDER, pdf_name)
    
    if not os.path.exists(pdf_path):
        return jsonify({"error": "Le fichier PDF spécifié n'existe pas"}), 404
    
    text_content = extract_text_from_pdf(pdf_path)
    return jsonify({"text": text_content})

# Route pour télécharger un fichier PDF
@app.route('/download_pdf', methods=['GET'])
def download_pdf():
    pdf_name = request.args.get('filename')
    if not pdf_name:
        return jsonify({"error": "Aucun nom de fichier spécifié"}), 400
    
    if not os.path.exists(os.path.join(PDF_FOLDER, pdf_name)):
        return jsonify({"error": "Le fichier PDF spécifié n'existe pas"}), 404
    
    # Envoie le fichier directement en pièce jointe
    return send_from_directory(PDF_FOLDER, pdf_name, as_attachment=True)

# Fonction pour extraire le texte d'un PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf:
        for page_num in range(pdf.page_count):
            page = pdf[page_num]
            text += page.get_text()
    return text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
