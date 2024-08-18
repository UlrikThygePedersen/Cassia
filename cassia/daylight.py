import pandas as pd  # type:ignore
from astral import LocationInfo
from astral.sun import sun
from datetime import timedelta, datetime
from typing import List, Tuple


def get_daylight_windows_corrected(
    latitude: float, longitude: float, start_date: pd.Timestamp, days: int = 14
) -> List[Tuple[pd.Timestamp, pd.Timestamp]]:
    # Create location object
    location = LocationInfo(latitude=latitude, longitude=longitude)

    daylight_windows = []

    for i in range(days):
        current_date = start_date + timedelta(days=i)
        s = sun(location.observer, date=current_date.date())

        # Retrieve sunrise and sunset times
        sunrise = s["sunrise"].replace(tzinfo=None)
        sunset = s["sunset"].replace(tzinfo=None)

        # Ensure sunrise comes before sunset; if not, swap them
        if sunrise > sunset:
            sunrise, sunset = sunset, sunrise

        daylight_windows.append((sunrise, sunset))

    return daylight_windows


# Function to format windows consistently
def format_windows(
    windows: List[Tuple[datetime, datetime]],
) -> List[Tuple[pd.Timestamp, pd.Timestamp]]:
    # Convert datetime to pd.Timestamp to match the format of tidal windows
    formatted_windows = [
        (pd.Timestamp(start), pd.Timestamp(end)) for start, end in windows
    ]
    return formatted_windows


# Function to combine tidal and daylight windows
def combine_tidal_and_daylight_windows(
    tidal_windows: List[Tuple[pd.Timestamp, pd.Timestamp]],
    daylight_windows: List[Tuple[pd.Timestamp, pd.Timestamp]],
) -> List[Tuple[pd.Timestamp, pd.Timestamp]]:
    combined_windows = []

    for tidal_start, tidal_end in tidal_windows:
        for daylight_start, daylight_end in daylight_windows:
            # Find overlap between tidal and daylight windows
            overlap_start = max(tidal_start, daylight_start)
            overlap_end = min(tidal_end, daylight_end)

            if overlap_start < overlap_end:
                combined_windows.append((overlap_start, overlap_end))

    return combined_windows
