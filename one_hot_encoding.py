import pickle
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

def apply_one_hot_encoding(df: pd.DataFrame, columns: list, save_path: str = None):
    """
    Fit and apply OneHotEncoder to specified columns.
    Optionally save the encoder as a pickle file.
    """
    ohe = OneHotEncoder(sparse=False, handle_unknown='ignore')
    ohe.fit(df[columns].astype(str))

    feature_names = ohe.get_feature_names_out(columns)
    encoded = ohe.transform(df[columns].astype(str))
    ohe_df = pd.DataFrame(encoded, columns=feature_names, index=df.index)

    df = df.drop(columns, axis=1)
    df = pd.concat([df, ohe_df], axis=1)

    if save_path:
        with open(save_path, 'wb') as f:
            pickle.dump(ohe, f)

    return df, ohe
