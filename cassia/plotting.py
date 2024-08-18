import pandas as pd  # type:ignore
from typing import List, Tuple
import matplotlib.pyplot as plt


def show_plot_tidal_windows(
    time_range: pd.DatetimeIndex,
    total_depths: List[float],
    vessel_draught: float,
    tidal_windows: List[Tuple[pd.Timestamp, pd.Timestamp]],
    port_name: str,
):
    plt.figure(figsize=(14, 7))

    plt.plot(time_range, total_depths, label="Total Depth (Harbor Depth + Tide)")
    plt.axhline(
        y=vessel_draught,
        color="r",
        linestyle="--",
        label=f"Vessel Draught ({vessel_draught} m)",
    )

    for tidal_start, tidal_end in tidal_windows:
        plt.axvspan(
            tidal_start, tidal_end, color="blue", alpha=0.2, label="Tidal Window"
        )

    plt.xlabel("Time")
    plt.ylabel("Water Depth (meters)")
    plt.title(f"Tidal Windows at {port_name}")
    plt.legend(loc="upper right")
    plt.show()


def show_plot_combined_windows(
    time_range: pd.DatetimeIndex,
    total_depths: List[float],
    vessel_draught: float,
    tidal_windows: List[Tuple[pd.Timestamp, pd.Timestamp]],
    daylight_windows: List[Tuple[pd.Timestamp, pd.Timestamp]],
    combined_windows: List[Tuple[pd.Timestamp, pd.Timestamp]],
    port_name: str,
):
    plt.figure(figsize=(14, 7))

    # Check for matching lengths between time_range and total_depths
    if len(time_range) != len(total_depths):
        raise ValueError("time_range and total_depths must have the same length.")

    plt.plot(time_range, total_depths, label="Total Depth (Harbor Depth + Tide)")
    plt.axhline(
        y=vessel_draught,
        color="r",
        linestyle="--",
        label=f"Vessel Draught ({vessel_draught} m)",
    )

    # To avoid duplicate labels in the legend
    tidal_label_done = False
    daylight_label_done = False
    combined_label_done = False

    # Highlight tidal windows
    for tidal_start, tidal_end in tidal_windows:
        if not tidal_label_done:
            plt.axvspan(
                tidal_start, tidal_end, color="blue", alpha=0.2, label="Tidal Window"
            )
            tidal_label_done = True
        else:
            plt.axvspan(tidal_start, tidal_end, color="blue", alpha=0.2)

    # Highlight daylight windows
    for daylight_start, daylight_end in daylight_windows:
        if not daylight_label_done:
            plt.axvspan(
                daylight_start,
                daylight_end,
                color="yellow",
                alpha=0.2,
                label="Daylight Window",
            )
            daylight_label_done = True
        else:
            plt.axvspan(daylight_start, daylight_end, color="yellow", alpha=0.2)

    # Highlight combined navigable windows
    for combined_start, combined_end in combined_windows:
        if not combined_label_done:
            plt.axvspan(
                combined_start,
                combined_end,
                color="green",
                alpha=0.5,
                label="Combined Navigable Window",
            )
            combined_label_done = True
        else:
            plt.axvspan(combined_start, combined_end, color="green", alpha=0.5)

    plt.xlabel("Time")
    plt.ylabel("Water Depth (meters)")
    plt.title(f"Tidal and Daylight Restriction Windows at {port_name}")
    plt.legend(loc="upper right")
    plt.show()
