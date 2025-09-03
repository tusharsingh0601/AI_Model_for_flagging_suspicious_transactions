import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(42)
N = 500

def gen_data(n=N):
    merchants = ["Amazon","Target","Shell","McDonalds","ATM"]
    cities = ["NY","LA","Chicago","Houston","Miami"]
    rows = []
    for i in range(n):
        amt = np.random.uniform(5, 1000)
        hist = np.random.uniform(20, 500)
        fraud = int(np.random.rand() < 0.1)
        rows.append({
            "id": i+1,
            "timestamp": (datetime.now()-timedelta(minutes=i)).isoformat(),
            "customer_id": f"CUST{np.random.randint(1000,9999)}",
            "merchant_category": np.random.choice(merchants),
            "city": np.random.choice(cities),
            "amount": amt,
            "historical_avg_amount": hist,
            "txn_count_24h": np.random.randint(1,20),
            "ip_risk_score": np.random.rand(),
            "card_present": np.random.randint(0,2),
            "is_fraud": fraud
        })
    return pd.DataFrame(rows)

df = gen_data()
os.makedirs("data", exist_ok=True)
df.to_csv("data/transactions.csv", index=False)
print("✅ transactions.csv generated")
