import os
import requests
import time

TOKEN = os.environ["TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

# message test au démarrage
send("🚀 BOT CONNECTÉ AVEC SUCCÈS")

# boucle toutes les heures
while True:
    send("⏰ BOT ACTIF - TEST HEURE")
    time.sleep(3600)
