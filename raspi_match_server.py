from flask import Flask, jsonify
import subprocess
import requests
from pathlib import Path
from gpiozero import LED
import time
from threading import Timer

# === Config ===
app = Flask(__name__)
PHOTO_PATH = "/tmp/photo.jpg"
LAPTOP_URL = "http://<IP_DEL_LAPTOP>:5000/analyze"  # << CAMBIA IP!
led_match = LED(17)
led_no_match = LED(22)

# === Funzione: scatta con libcamera ===
def capture_photo():
    print("📸 Scatto foto con libcamera-still...")
    result = subprocess.run([
        "libcamera-still",
        "-t", "1000",         # 1 secondo per stabilizzare
        "--nopreview",        # Nessuna preview grafica
        "--width", "640",     # Risoluzione stabile
        "--height", "480",
        "-o", PHOTO_PATH
    ], capture_output=True)

    if result.returncode != 0:
        print("❌ Errore libcamera-still:", result.stderr.decode())
        return False

    return Path(PHOTO_PATH).exists()

# === Funzione: spegne i LED ===
def turn_off_leds():
    led_match.off()
    led_no_match.off()
    print("💡 LED spenti automaticamente dopo 10 secondi.")

# === Funzione: controlla LED ===
def show_result_led(result):
    led_match.off()
    led_no_match.off()

    if result == "MATCH":
        led_match.on()
    elif result == "NO MATCH":
        led_no_match.on()

    # Timer per spegnere i LED dopo 10 secondi
    Timer(10.0, turn_off_leds).start()

# === Endpoint per attivare scansione ===
@app.route("/scan", methods=["GET"])
def scan_and_send():
    if not capture_photo():
        return jsonify({"error": "camera_failed"}), 500

    try:
        with open(PHOTO_PATH, "rb") as img:
            files = {"image": ("photo.jpg", img, "image/jpeg")}
            print("\U0001F4E4 Invio al laptop...")
            r = requests.post(LAPTOP_URL, files=files, timeout=10)

        if r.ok:
            result = r.json().get("result", "UNKNOWN")
            print("✅ RISULTATO:", result)
            show_result_led(result)
            return jsonify({"result": result}), 200
        else:
            print("❌ Risposta NON OK:", r.status_code)
            return jsonify({"error": "processing_error"}), 500
    except Exception as e:
        print("❌ Errore connessione:", e)
        return jsonify({"error": "connection_failed"}), 500

if __name__ == "__main__":
    led_match.off()
    led_no_match.off()
    app.run(host="0.0.0.0", port=8080)
