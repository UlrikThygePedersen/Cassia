import pandas as pd  # type:ignore
from scipy.interpolate import interp1d  # type:ignore
from typing import List, Tuple


def calculate_tidal_windows(
    imo: int,
    unlocode: str,
    arrival_time: pd.Timestamp,
    vessels_dispatcher,
    ports_dispatcher,
    tide_heights_df,
) -> Tuple[List[Tuple[pd.Timestamp, pd.Timestamp]], pd.DatetimeIndex, List[float]]:
    vessel = vessels_dispatcher[imo]
    port = ports_dispatcher[unlocode]

    approach_depth = port.approach_mllw_meters

    port_tide_data = tide_heights_df[tide_heights_df["PORT_NAME"] == port.name]
    port_tide_data["TIDE_DATETIME"] = pd.to_datetime(port_tide_data["TIDE_DATETIME"])
    port_tide_data = port_tide_data.sort_values(by="TIDE_DATETIME")
    port_tide_data["TIMESTAMP"] = port_tide_data["TIDE_DATETIME"].apply(
        lambda x: x.timestamp()
    )

    interpolation_function = interp1d(
        port_tide_data["TIMESTAMP"],
        port_tide_data["TIDE_HEIGHT_MT"],
        kind="linear",
        fill_value="extrapolate",
    )

    time_range = pd.date_range(start=arrival_time, periods=14 * 24 * 60, freq="T")
    time_stamps = time_range.map(lambda x: x.timestamp())
    interpolated_tide_heights = interpolation_function(time_stamps)

    total_depths = approach_depth + interpolated_tide_heights
    can_navigate = total_depths > vessel.draught

    tidal_windows = []
    window_start = None

    for i in range(len(can_navigate)):
        if can_navigate[i] and window_start is None:
            window_start = time_range[i]
        elif not can_navigate[i] and window_start is not None:
            tidal_windows.append((window_start, time_range[i - 1]))
            window_start = None

    if window_start is not None:
        tidal_windows.append((window_start, time_range[-1]))

    return tidal_windows, time_range, total_depths
