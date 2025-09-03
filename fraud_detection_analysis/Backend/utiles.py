import pandas as pd

CATEGORICAL = ["merchant_category","city","card_present"]

def feature_engineer(df):
    X = df[["amount","ip_risk_score","historical_avg_amount","txn_count_24h"]].copy()
    X["amount_to_avg"]=X["amount"]/(X["historical_avg_amount"]+1e-6)
    cat=pd.get_dummies(df[CATEGORICAL].astype(str),prefix_sep="__")
    X=pd.concat([X,cat],axis=1)
    return X.fillna(0), df["is_fraud"]
