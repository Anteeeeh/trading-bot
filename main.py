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
    df = pd.read_csv("portfolio.csv")

    for _, row in df.iterrows():
        data = yf.download(row["ticker"], period="1d", interval="1h")

        if data.empty:
            continue

        price = float(data["Close"].iloc[-1])
        change = ((price - row["pru"]) / row["pru"]) * 100

        if change > 5:
            signal = "🚀 OPPORTUNITÉ (RENFORCER)"
            send(f"{row['asset']} → {signal}\nPerf: {round(change,2)}%")

        elif change < -5:
            signal = "⚠️ RISQUE (SURVEILLER / VENDRE)"
            send(f"{row['asset']} → {signal}\nPerf: {round(change,2)}%")

print("✅ BOT ANALYSE LANCÉ")

while True:
    analyze()
    time.sleep(3600)
