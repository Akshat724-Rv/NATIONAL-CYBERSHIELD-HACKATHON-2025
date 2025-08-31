import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder

def apply_label_encoding(df: pd.DataFrame, columns: list, save_path: str = None):
    """
    Fit and apply LabelEncoder to specified columns.
    Optionally save the encoders as a pickle file.
    """
    encoders = {}
    for col in columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le

    if save_path:
        with open(save_path, 'wb') as f:
            pickle.dump(encoders, f)

    return df, encoders
