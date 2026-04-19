from flask import Flask, render_template
import pandas as pd
import yfinance as yf

app = Flask(__name__)

def get_data():
    df = pd.read_csv("portfolio.csv")
    results = []
    total_value = 0
    total_cost = 0

    for _, row in df.iterrows():
        data = yf.download(row["ticker"], period="7d", interval="1h", progress=False)

        if data.empty:
            continue

        # correction bug yfinance
        if isinstance(data.columns, pd.MultiIndex):
            close = data["Close"].iloc[:, 0]
        else:
            close = data["Close"]

        close = close.dropna()

        if len(close) == 0:
            continue

        price = float(close.iloc[-1])
        change = ((price - row["pru"]) / row["pru"]) * 100

        chart = close.tail(24).tolist()

        results.append({
            "asset": row["asset"],
            "ticker": row["ticker"],
            "price": round(price, 2),
            "pru": row["pru"],
            "change": round(change, 2),
            "chart": chart
        })

        total_value += price * row["quantity"]
        total_cost += row["pru"] * row["quantity"]

    perf = ((total_value - total_cost) / total_cost) * 100 if total_cost else 0

    return results, round(total_value, 2), round(perf, 2)


@app.route("/")
def dashboard():
    data, value, perf = get_data()
    return render_template("index.html", data=data, value=value, perf=perf)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
