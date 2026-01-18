import pandas as pd


def make_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["price_x_ads"] = df["price"] * df["ads_spend"]
    return df
