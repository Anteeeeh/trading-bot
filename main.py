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

def get_price(data):
    try:
        # 🔥 FIX PRINCIPAL
        if isinstance(data.columns, pd.MultiIndex):
            close = data["Close"].iloc[:, 0]  # prend la bonne colonne
        else:
            close = data["Close"]

        close = close.dropna()

        if len(close) == 0:
            return None

        return float(close.iloc[-1])

    except Exception as e:
        print("❌ erreur extraction prix:", e)
        return None


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
            pru = float(row["pru"])

            print(f"➡️ Analyse {asset} ({ticker})")

            data = yf.download(
                ticker,
                period="1d",
                interval="1h",
                auto_adjust=True,
                progress=False
            )

            if data is None or data.empty:
                print(f"⚠️ Pas de données pour {ticker}")
                continue

            price = get_price(data)

            if price is None:
                print(f"⚠️ Prix introuvable pour {ticker}")
                continue

            change = ((price - pru) / pru) * 100

            print(f"💰 {asset} prix: {price} | perf: {round(change,2)}%")

            # 🧪 TEST TEMPORAIRE
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
