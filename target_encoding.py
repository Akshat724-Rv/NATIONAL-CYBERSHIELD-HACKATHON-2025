import pickle
import pandas as pd
from category_encoders import TargetEncoder

def apply_target_encoding(
    df: pd.DataFrame,
    categorical_cols: list,
    target_col: str,
    save_path: str = None
):
    """
    Fit and apply TargetEncoder to specified categorical columns using target_col.
    Optionally save the encoder as a pickle file.
    """
    te = TargetEncoder(cols=categorical_cols)
    df[categorical_cols] = te.fit_transform(df[categorical_cols], df[target_col])

    if save_path:
        with open(save_path, 'wb') as f:
            pickle.dump(te, f)

    return df, te
