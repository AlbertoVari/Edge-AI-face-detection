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

________________________________________________

Procedura di lancio :

Sul Laptop, avvia prima il server Flask per l’analisi:

python face_analysis_server.py

Ora il laptop è in ascolto sulla porta 5000 e pronto a ricevere foto.

Assicurati che rimanga attivo (non chiudere il terminale).

Sul Raspberry Pi, lancia il server Flask con camera e led:

python3 raspi_match_server.py

A questo punto, il Raspberry è pronto a ricevere richieste su http://<IP_PI>:8080/scan.

Avvio del processo di riconoscimento:

Invia una richiesta al Raspberry (da un altro terminale, cron, sensore o script sul laptop) con:

curl http://<IP_DEL_PI>:8080/scan
Il Raspberry scatta la foto, la invia al laptop, riceve il risultato e accende il LED corrispondente.

⚠️ Cosa succede in ordine:
Il laptop deve essere pronto a ricevere (face_analysis_server.py)

Il Raspberry deve poter reindirizzare le foto (raspi_match_server.py)

Il comando curl (o uno script) riavvia il ciclo di scatto → invio → risultato → LED



📤 Invio al laptop per analisi

💡 Controllo dei LED su GPIO 17 (MATCH) e 22 (NO MATCH)

Ricordati di sostituire "<IP_DEL_LAPTOP>" con l’indirizzo IP reale del tuo laptop.
