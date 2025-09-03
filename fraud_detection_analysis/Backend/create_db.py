import pandas as pd, sqlite3, os

os.makedirs("db", exist_ok=True)
df = pd.read_csv("data/transactions.csv")
conn = sqlite3.connect("db/transactions.db")
df.to_sql("transactions", conn, if_exists="replace", index=False)
conn.close()
print("✅ transactions.db created")
