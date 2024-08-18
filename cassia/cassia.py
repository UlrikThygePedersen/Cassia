import pandas as pd  # type:ignore

from cassia.daylight import (
    get_daylight_windows_corrected,
    combine_tidal_and_daylight_windows,
    format_windows,
)
from cassia.dispatchers import ports_dispatcher, vessels_dispatcher
from cassia.interpolation import calculate_tidal_windows
from cassia.plotting import show_plot_tidal_windows, show_plot_combined_windows

from cassia.helpers import get_tide_data


class Cassia:
    def __init__(
        self,
        vessels_dispatcher: dict = vessels_dispatcher,
        ports_dispatcher: dict = ports_dispatcher,
        tide_heights_df: pd.DataFrame = get_tide_data(),
    ) -> None:
        self.tide_heights_df = tide_heights_df
        self.vessels_dispatcher = vessels_dispatcher
        self.ports_dispatcher = ports_dispatcher

    def get_tidal_windows(self, imo: int, unlocode: str, arrival_time: pd.Timestamp):
        return calculate_tidal_windows(
            imo=imo,
            unlocode=unlocode,
            arrival_time=arrival_time,
            vessels_dispatcher=self.vessels_dispatcher,
            ports_dispatcher=self.ports_dispatcher,
            tide_heights_df=self.tide_heights_df,
        )

    def get_combined_windows(
        self, imo: int, unlocode: str, arrival_time: pd.Timestamp, days: int = 14
    ):
        # Calculate tidal windows
        tidal_windows, time_range, total_depths = self.get_tidal_windows(
            imo, unlocode, arrival_time
        )

        # Get daylight windows
        port = self.ports_dispatcher[unlocode]
        daylight_windows = get_daylight_windows_corrected(
            port.latitude, port.longitude, arrival_time, days
        )

        # Format daylight windows
        formatted_daylight_windows = format_windows(daylight_windows)

        # Combine tidal and daylight windows
        combined_windows = combine_tidal_and_daylight_windows(
            tidal_windows, formatted_daylight_windows
        )

        self.combined_windows = combined_windows
        self.time_range = time_range
        self.total_depths = total_depths
        self.tidal_windows = tidal_windows
        self.formatted_daylight_windows = formatted_daylight_windows

        return combined_windows

    def plot_tidal_windows(
        self,
        imo,
        unlocode,
    ):
        return show_plot_tidal_windows(
            time_range=self.time_range,
            total_depths=self.total_depths,
            vessel_draught=self.vessels_dispatcher.get(imo).draught,
            tidal_windows=self.tidal_windows,
            port_name=self.ports_dispatcher.get(unlocode).name,
        )

    def plot_combined_windows(
        self,
        imo,
        unlocode,
    ):
        return show_plot_combined_windows(
            time_range=self.time_range,
            total_depths=self.total_depths,
            vessel_draught=self.vessels_dispatcher.get(imo).draught,
            tidal_windows=self.tidal_windows,
            daylight_windows=self.formatted_daylight_windows,
            combined_windows=self.combined_windows,
            port_name=self.ports_dispatcher.get(unlocode).name,
        )
