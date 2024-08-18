import pandas as pd  # type:ignore


def get_tide_data():
    tide_heights_df = pd.read_csv("../assets/tide_heights.csv")
    return tide_heights_df
