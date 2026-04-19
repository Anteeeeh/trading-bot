import os
import pandas as pd
import yfinance as yf
import requests
import time

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send(msg):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except Exception as e:
        print("Erreur Telegram:", e)

def analyze():
    print("🔍 Lancement analyse...")

    try:
        df = pd.read_csv("portfolio.csv")
        print("✅ Portfolio chargé")
    except Exception as e:
        print("❌ Erreur CSV:", e)
        return

    for _, row in df.iterrows():
        try:
            ticker = row["ticker"]
            asset = row["asset"]

            print(f"➡️ Analyse {asset}")

            data = yf.download(ticker, period="1d", interval="1h")

            if data.empty:
                print(f"⚠️ Pas de données pour {ticker}")
                continue

            price = float(data["Close"].iloc[-1])

            print(f"💰 {asset} prix: {price}")

            # test envoi
            send(f"TEST {asset} prix: {price}")

        except Exception as e:
            print(f"❌ Erreur sur {asset}:", e)

print("✅ BOT DÉMARRÉ")

while True:
    try:
        analyze()
    except Exception as e:
        print("❌ Erreur globale:", e)

    print("⏳ Pause 60 secondes")
    time.sleep(60)
