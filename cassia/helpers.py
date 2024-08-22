import pandas as pd  # type:ignore

from pathlib import Path
current_dir = Path(__file__).resolve().parent


tide_heights_csv_path = current_dir / '../assets/tide_heights.csv'


def get_tide_data():
    tide_heights_df = pd.read_csv(tide_heights_csv_path)
    return tide_heights_df
