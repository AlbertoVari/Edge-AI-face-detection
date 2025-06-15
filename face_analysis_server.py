from flask import Flask, request, jsonify
import cv2
import tempfile
import os
import subprocess

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def analyze():
    if 'image' not in request.files:
        return jsonify({"error": "No image part"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Salva temporaneamente
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        file.save(tmp.name)
        input_path = os.path.abspath(tmp.name)

    try:
        # Sposta immagine per main.py
        os.replace(input_path, "input.jpg")

        # Esegui main.py
        result = subprocess.run(["python", "main.py"], capture_output=True, text=True)

        # Analizza output testuale
        if "MATCH trovato" in result.stdout:
            return jsonify({"result": "MATCH"}), 200
        elif "NESSUN MATCH" in result.stdout:
            return jsonify({"result": "NO MATCH"}), 200
        else:
            print(result.stdout)
            return jsonify({"error": "output_not_parsed"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
