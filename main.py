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
        print("Erreur envoi Telegram:", e)

def analyze():
    try:
        df = pd.read_csv("portfolio.csv")
    except Exception as e:
        print("❌ erreur lecture CSV:", e)
        return

    for _, row in df.iterrows():
        try:
            ticker = row["ticker"]
            asset = row["asset"]
            pru = float(row["pru"])

            print(f"Analyse de {asset} ({ticker})")

            data = yf.download(ticker, period="1d", interval="1h")

            if data is None or data.empty:
                print(f"⚠️ aucune donnée pour {ticker}")
                continue

            price = float(data["Close"].iloc[-1])
            change = ((price - pru) / pru) * 100

            print(f"{asset} prix: {price} | perf: {round(change,2)}%")

            # ⚠️ TEST TEMPORAIRE (pour vérifier que ça envoie)
            if change > 0:
                send(f"📊 {asset}\nPrix: {price}\nPerf: {round(change,2)}%")

        except Exception as e:
            print(f"❌ erreur sur {row} :", e)

print("✅ BOT ANALYSE LANCÉ")

while True:
    try:
        analyze()
    except Exception as e:
        print("❌ erreur globale :", e)

    time.sleep(3600)
