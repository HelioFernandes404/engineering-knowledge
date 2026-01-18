import pandas as pd
from sales_forecast.features import make_features


def test_make_features_adds_column():
    df = pd.DataFrame({"price": [10.0], "ads_spend": [2.0]})
    out = make_features(df)
    assert out["price_x_ads"].iloc[0] == 20.0
