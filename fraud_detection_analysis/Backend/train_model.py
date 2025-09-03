import pandas as pd, joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv("data/transactions.csv")
df["amount_to_avg"] = df["amount"] / (df["historical_avg_amount"]+1e-6)

X = df[["amount","ip_risk_score","historical_avg_amount","txn_count_24h","amount_to_avg"]]
X = pd.get_dummies(pd.concat([X, df[["merchant_category","city","card_present"]]], axis=1))
y = df["is_fraud"]

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train,y_train)

joblib.dump({"model": model, "columns": X.columns.tolist()}, "backend/model.joblib")
print("✅ ML model trained & saved")
