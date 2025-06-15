# Edge-AI-face-detection
A Raspberry Pi-based Flask server captures an image with a CSI camera, sends it to a laptop running OpenVINO for facial recognition, and uses GPIO LEDs to indicate whether the face is recognized (MATCH) or not (NO MATCH)

🧠 Architettura finale confermata
🍓 Raspberry Pi (Flask Server):
Espone un endpoint HTTP (es. /scan)

Quando chiamato:

📸 Scatta una foto con libcamera

📤 Invia la foto al laptop

📥 Riceve il risultato (MATCH / NO MATCH)

🖨️ Lo stampa (o usa in GPIO, ecc.)

💻 Laptop (API Server):
Riceve immagine dal Raspberry

Esegue main.py

Ritorna il risultato (MATCH / NO MATCH)

✅ STEP 1 – Laptop (già pro
