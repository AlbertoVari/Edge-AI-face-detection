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

______________________________________

Riepilogo del ruolo del laptop:
Riceve un'immagine da Raspberry via HTTP POST

Esegue main.py (già pronto con OpenVINO)

Ritorna il risultato: {"result": "MATCH"} o {"result": "NO MATCH"}

face_analysis_server.py (da eseguire sul laptop)

_______________________________________

Comunicazione in rete
Assicurati che:

Il Raspberry conosca l’IP del laptop

Entrambi siano sulla stessa rete

Il laptop non abbia firewall che blocca la porta 5000

Puoi testare manualmente da Raspberry:

bash
Copia
Modifica
curl -X POST -F image=@/tmp/photo.jpg http://<IP_DEL_LAPTOP>:5000/analyze

____________________________________________

Il file raspi_match_server.py è stato aggiornato con:

🕒 Spegnimento automatico dei LED dopo 10 secondi

📸 Acquisizione immagine con libcamera

📤 Invio al laptop per analisi

💡 Controllo dei LED su GPIO 17 (MATCH) e 22 (NO MATCH)

Ricordati di sostituire "<IP_DEL_LAPTOP>" con l’indirizzo IP reale del tuo laptop.
