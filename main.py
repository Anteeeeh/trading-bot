import os
import pandas as pd
import yfinance as yf
import requests
import time

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def analyze():
    try:
        df = pd.read_csv("portfolio.csv")
    except Exception as e:
        print("❌ erreur lecture portfolio:", e)
        return

    for _, row in df.iterrows():
        try:
            data = yf.download(row["ticker"], period="1d", interval="1h")

            if data.empty:
                print(f"⚠️ pas de data pour {row['ticker']}")
                continue

            price = float(data["Close"].iloc[-1])
            change = ((price - row["pru"]) / row["pru"]) * 100

            print(f"{row['asset']} → {price} ({round(change,2)}%)")

            if change > 5:
                send(f"🚀 {row['asset']} opportunité\nPerf: {round(change,2)}%")

            elif change < -5:
                send(f"⚠️ {row['asset']} risque\nPerf: {round(change,2)}%")

        except Exception as e:
            print(f"❌ erreur sur {row['asset']}:", e)

print("✅ BOT ANALYSE LANCÉ")

while True:
    analyze()
    time.sleep(3600)
