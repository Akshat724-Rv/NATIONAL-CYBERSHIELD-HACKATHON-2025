# prepare_data.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
import os

# ===== 1. Create dummy CSV if missing =====
if not os.path.exists("transactions.csv"):
    np.random.seed(42)
    df_dummy = pd.DataFrame({
        "merchant": np.random.choice(["Amazon", "Walmart", "Target"], size=200),
        "amount": np.random.uniform(5, 500, size=200),
        "is_fraud": np.random.choice([0, 1], size=200, p=[0.9, 0.1])
    })
    df_dummy.to_csv("transactions.csv", index=False)
    print("⚠️ No transactions.csv found — created dummy dataset.")

# ===== 2. Load dataset =====
df = pd.read_csv("transactions.csv")

# ===== 3. Encode merchant =====
merchant_encoder = LabelEncoder()
df["merchant"] = merchant_encoder.fit_transform(df["merchant"])

# ===== 4. Split features/target =====
X = df.drop("is_fraud", axis=1)
y = df["is_fraud"]

# ===== 5. Train/test split =====
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ===== 6. Train model =====
model = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# ===== 7. Save model & encoder =====
joblib.dump(model, "model.pkl")
joblib.dump(merchant_encoder, "merchant_encoder.pkl")
print("✅ model.pkl and merchant_encoder.pkl saved.")

# ===== 8. Save encoded features =====
X_test.to_excel("encoded_test_features.xlsx", index=False)
print("✅ encoded_test_features.xlsx saved.")

# ===== 9. Quick accuracy check =====
acc = model.score(X_test, y_test)
print(f"📊 Model accuracy: {acc:.2%}")
