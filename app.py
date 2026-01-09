import os
import json
import requests
from flask import Flask, render_template, request

AML_ENDPOINT = os.getenv("AML_ENDPOINT_URL")  # e.g., https://<endpoint>/score
AML_KEY = os.getenv("AML_KEY")                # key or token
THRESHOLD = float(os.getenv("THRESHOLD", "0.5"))

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        age = float(request.form.get("age"))
        debt_ratio = float(request.form.get("DebtRatio"))
        monthly_income = float(request.form.get("MonthlyIncome"))
        times_90 = float(request.form.get("NumberOfTimes90DaysLate"))

        payload = {
            "input_data": {
                "columns": ["age", "DebtRatio", "MonthlyIncome", "NumberOfTimes90DaysLate"],
                "index": [0],
                "data": [[age, debt_ratio, monthly_income, times_90]]
            }
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {AML_KEY}"
        }

        resp = requests.post(AML_ENDPOINT, headers=headers, data=json.dumps(payload), timeout=10)
        resp.raise_for_status()
        out = resp.json()

        proba = float(out.get("probabilities", [0])[0])
        risk_class = "高風險" if proba >= THRESHOLD else "低風險"

        return render_template("index.html", result={
            "risk_class": risk_class,
            "probability": round(proba * 100, 2)
        })
    except Exception as e:
        return render_template("index.html", result={"risk_class": "錯誤", "probability": 0}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
