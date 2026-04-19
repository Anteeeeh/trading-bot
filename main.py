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
        print("❌ Erreur Telegram:", e)

def analyze():
    print("🔍 Lancement analyse...")

    try:
        df = pd.read_csv("portfolio.csv")
        print("✅ Portfolio chargé")
    except Exception as e:
        print("❌ Erreur lecture CSV:", e)
        return

    for _, row in df.iterrows():
        try:
            ticker = row["ticker"]
            asset = row["asset"]
            pru = float(row["pru"])

            print(f"➡️ Analyse {asset} ({ticker})")

            data = yf.download(ticker, period="1d", interval="1h")

            if data is None or data.empty:
                print(f"⚠️ Pas de données pour {ticker}")
                continue

            # 🔒 VERSION SAFE
            close_data = data["Close"].dropna()

            if len(close_data) == 0:
                print(f"⚠️ Pas de prix exploitable pour {ticker}")
                continue

            price = float(close_data.values[-1])
            change = ((price - pru) / pru) * 100

            print(f"💰 {asset} prix: {price} | perf: {round(change,2)}%")

            # 🧪 TEST TEMPORAIRE (envoie toujours un message)
            send(f"📊 {asset}\nPrix: {price}\nPerf: {round(change,2)}%")

        except Exception as e:
            print(f"❌ Erreur sur {row['asset']} :", e)

print("✅ BOT ANALYSE LANCÉ")

while True:
    try:
        analyze()
    except Exception as e:
        print("❌ Erreur globale :", e)

    print("⏳ Pause 60 secondes")
    time.sleep(60)
