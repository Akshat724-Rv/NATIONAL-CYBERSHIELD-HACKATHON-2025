from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import os

app = Flask(__name__)

MODEL_PATH = "model.pkl"
MERCHANT_ENCODER_PATH = "merchant_encoder.pkl"

if not os.path.exists(MODEL_PATH) or not os.path.exists(MERCHANT_ENCODER_PATH):
    raise FileNotFoundError("Model or encoder file missing. Run prepare_data.py first.")

model = joblib.load(MODEL_PATH)
merchant_encoder = joblib.load(MERCHANT_ENCODER_PATH)

@app.route("/", methods=["GET"])
def index():
    merchants = list(merchant_encoder.classes_)
    return render_template("index.html", merchants=merchants)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        merchant = request.form.get("merchant")
        file = request.files.get("csv_file")
        threshold = float(request.form.get("threshold", 0.5))

        if not merchant or not file:
            return jsonify({"error": "Please select a merchant and upload a CSV file"}), 400

        df = pd.read_csv(file)

        if 'is_fraud' in df.columns:
            df = df.drop(columns=['is_fraud'])

        encoded_val = merchant_encoder.transform([merchant])[0]
        df["merchant"] = [encoded_val] * len(df)

        expected_cols = model.feature_names_in_
        missing = set(expected_cols) - set(df.columns)
        if missing:
            return jsonify({"error": f"Missing columns: {', '.join(missing)}"}), 400
        df = df[expected_cols]

        scores = model.predict_proba(df)[:, 1]
        preds = (scores >= threshold).astype(int)

        results = [
            {"index": i + 1, "score": round(float(score), 4), "prediction": bool(pred)}
            for i, (score, pred) in enumerate(zip(scores, preds))
        ]

        return render_template(
            "results.html",
            results=results,
            merchant=merchant,
            threshold=threshold
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
