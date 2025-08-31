def detect_suspicious_transactions(df, merchant_name):
    merchant_txns = df[df['merchant'] == merchant_name]
    suspicious = merchant_txns[(merchant_txns['is_suspicious_amount'] == 1) |
                               (merchant_txns['is_suspicious_time'] == 1) |
                               (merchant_txns['is_high_risk_merchant'] == 1) |
                               (merchant_txns['is_high_risk_city'] == 1)]
    total_suspicious_amount = suspicious['amount'].sum()
    return {"total_suspicious_amount": total_suspicious_amount}