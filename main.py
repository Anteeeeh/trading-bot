import os
import requests
import time

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not TOKEN or not CHAT_ID:
    print("❌ TOKEN ou CHAT_ID manquant")
    exit()

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

print("✅ BOT DÉMARRÉ")

send("🚀 BOT CONNECTÉ AVEC SUCCÈS")

while True:
    send("⏰ BOT ACTIF - TEST HEURE")
    time.sleep(3600)
