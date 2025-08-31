import os
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def train_model(
    feature_path: str = 'encoded_train_features.xlsx',
    target_path:  str = 'encoded_train_target.xlsx',
    model_output: str = 'models/model.pkl'
):
    os.makedirs(os.path.dirname(model_output), exist_ok=True)

    feat_exists = os.path.exists(feature_path)
    targ_exists = os.path.exists(target_path)

    if feat_exists and targ_exists:
        # 1a. load separate files
        df_feat = pd.read_excel(feature_path)
        df_tar  = pd.read_excel(target_path)
        print(f"▶ Loaded features {df_feat.shape}, targets {df_tar.shape}")

        # 2a. try merge by TransactionID or align by index
        if 'TransactionID' in df_feat.columns and 'TransactionID' in df_tar.columns:
            df = pd.merge(df_feat, df_tar, on='TransactionID', how='inner')
            print(f"✔ Merged on TransactionID → {df.shape}")
        elif df_feat.shape[0] == df_tar.shape[0]:
            df = pd.concat([
                df_feat.reset_index(drop=True),
                df_tar.reset_index(drop=True)
            ], axis=1)
            print("✔ Concatenated by index")
        else:
            raise ValueError(
                "Row counts differ and no TransactionID: cannot align features & targets."
            )

        # identify the single target column
        tar_cols = [c for c in df_tar.columns if c != 'TransactionID']
        if len(tar_cols) != 1:
            raise ValueError(f"Expected one target column but found {tar_cols}")
        target_col = tar_cols[0]

        X = df.drop(columns=[target_col, 'TransactionID', 'Time'], errors='ignore')
        y = df[target_col]

    elif not feat_exists and targ_exists:
        # 1b. fallback to a combined sheet
        df = pd.read_excel(target_path)
        print(f"▶ Loaded combined dataset {df.shape}")

        if 'label' not in df.columns:
            raise ValueError("Combined file missing a 'label' column")
        X = df.drop(columns=['label', 'TransactionID', 'Time'], errors='ignore')
        y = df['label']

    else:
        raise FileNotFoundError(
            f"Expected:\n - features: {feature_path}\n - targets:  {target_path}\n"
            "At least target_path must exist."
        )

    # 3. split, train, eval
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    acc = clf.score(X_test, y_test)
    print(f"✔ Test accuracy: {acc:.4f}")

    # 4. serialize
    with open(model_output, 'wb') as f:
        pickle.dump(clf, f)
    print(f"✔ Model saved → {model_output}")


if __name__ == '__main__':
    train_model()
