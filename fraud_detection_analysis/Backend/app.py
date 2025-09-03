from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3, joblib, pandas as pd
from fastapi.middleware.cors import CORSMiddleware  # <-- Make sure this line is present

app = FastAPI(title="Fraud Detection Prototype")

# Your app.add_middleware code follows...

# Add this CORS middleware block
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

DB = "db/transactions.db"
MODEL_PATH = "Backend/model.joblib"

# Load ML model
bundle = joblib.load(MODEL_PATH)
model, model_cols = bundle["model"], bundle["columns"]

# Request schema for prediction
class PredictIn(BaseModel):
    amount: float
    ip_risk_score: float
    historical_avg_amount: float
    txn_count_24h: int
    merchant_category: str
    city: str
    card_present: int

@app.get("/transactions")
def get_transactions(limit: int = 20, offset: int = 0):
    conn = sqlite3.connect(DB)
    df = pd.read_sql(
        f"SELECT * FROM transactions ORDER BY timestamp DESC LIMIT {limit} OFFSET {offset}", conn
    )
    conn.close()
    return df.to_dict(orient="records")

@app.get("/alerts")
def get_alerts(limit: int = 5):
    conn = sqlite3.connect(DB)
    df = pd.read_sql(
        f"SELECT * FROM transactions WHERE is_fraud=1 ORDER BY timestamp DESC LIMIT {limit}", conn
    )
    conn.close()
    return df.to_dict(orient="records")

@app.post("/predict")
def predict(inp: PredictIn):
    # Build features
    x = {
        "amount": inp.amount,
        "ip_risk_score": inp.ip_risk_score,
        "historical_avg_amount": inp.historical_avg_amount,
        "txn_count_24h": inp.txn_count_24h,
        "amount_to_avg": inp.amount / (inp.historical_avg_amount + 1e-6),
    }
    for col in model_cols:
        if "__" in col:
            prefix, val = col.split("__", 1)
            x[col] = int(
                (prefix == "merchant_category" and val == inp.merchant_category)
                or (prefix == "city" and val == inp.city)
                or (prefix == "card_present" and val == str(inp.card_present))
            )

    X = pd.DataFrame([x])[model_cols]
    prob = model.predict_proba(X)[0, 1]
    return {"score": float(prob), "is_suspicious": bool(prob > 0.5)}

@app.get("/metrics")
def metrics():
    conn = sqlite3.connect(DB)
    df = pd.read_sql("SELECT * FROM transactions", conn)
    conn.close()
    return {
        "total": len(df),
        "flagged": int(df["is_fraud"].sum()),
        "accuracy": 94.7,   # mock for demo
        "false_positive_rate": 2.3,
    }
