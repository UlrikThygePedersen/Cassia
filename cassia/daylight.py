import pandas as pd  # type:ignore
from astral import LocationInfo
from astral.sun import sun
from datetime import timedelta, datetime
from typing import List, Tuple


def get_daylight_windows_corrected(
    latitude: float, longitude: float, start_date: pd.Timestamp, days: int = 14
) -> List[Tuple[pd.Timestamp, pd.Timestamp]]:
    location = LocationInfo(latitude=latitude, longitude=longitude)

    daylight_windows = []

    for i in range(days):
        current_date = start_date + timedelta(days=i)
        s = sun(location.observer, date=current_date.date())

        sunrise = s["sunrise"].replace(tzinfo=None)
        sunset = s["sunset"].replace(tzinfo=None)

        if sunrise > sunset:
            sunrise, sunset = sunset, sunrise

        daylight_windows.append((sunrise, sunset))

    return daylight_windows


def format_windows(
    windows: List[Tuple[datetime, datetime]],
) -> List[Tuple[pd.Timestamp, pd.Timestamp]]:
    formatted_windows = [
        (pd.Timestamp(start), pd.Timestamp(end)) for start, end in windows
    ]
    return formatted_windows


def combine_tidal_and_daylight_windows(
    tidal_windows: List[Tuple[pd.Timestamp, pd.Timestamp]],
    daylight_windows: List[Tuple[pd.Timestamp, pd.Timestamp]],
) -> List[Tuple[pd.Timestamp, pd.Timestamp]]:
    combined_windows = []

    for tidal_start, tidal_end in tidal_windows:
        for daylight_start, daylight_end in daylight_windows:
            overlap_start = max(tidal_start, daylight_start)
            overlap_end = min(tidal_end, daylight_end)

            if overlap_start < overlap_end:
                combined_windows.append((overlap_start, overlap_end))

    return combined_windows
