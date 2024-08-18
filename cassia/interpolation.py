import pandas as pd #type:ignore
from scipy.interpolate import interp1d #type:ignore
from typing import List, Tuple

def calculate_tidal_windows(imo: int, unlocode: str, arrival_time: pd.Timestamp, tide_heights_df: pd.DataFrame, 
                            vessels_dispatcher: dict, ports_dispatcher: dict) -> Tuple[List[Tuple[pd.Timestamp, pd.Timestamp]], pd.DatetimeIndex, List[float]]:
    # Retrieve vessel and port data
    vessel = vessels_dispatcher[imo]
    port = ports_dispatcher[unlocode]

    # Extract port information
    approach_depth = port.approach_mllw_meters

    # Filter tide heights for the specified port
    port_tide_data = tide_heights_df[tide_heights_df['PORT_NAME'] == port.name]

    # Convert TIDE_DATETIME to datetime
    port_tide_data['TIDE_DATETIME'] = pd.to_datetime(port_tide_data['TIDE_DATETIME'])

    # Sort the data by time
    port_tide_data = port_tide_data.sort_values(by='TIDE_DATETIME')

    # Convert datetime to a numerical format (e.g., Unix timestamp)
    port_tide_data['TIMESTAMP'] = port_tide_data['TIDE_DATETIME'].apply(lambda x: x.timestamp())

    # Perform linear interpolation
    interpolation_function = interp1d(port_tide_data['TIMESTAMP'], port_tide_data['TIDE_HEIGHT_MT'], 
                                      kind='linear', fill_value="extrapolate")

    # Generate the time range for the next 14 days with minute intervals
    time_range = pd.date_range(start=arrival_time, periods=14*24*60, freq='T')
    time_stamps = time_range.map(lambda x: x.timestamp())
    interpolated_tide_heights = interpolation_function(time_stamps)

    # Calculate the total depths
    total_depths = approach_depth + interpolated_tide_heights

    # Determine if the vessel can navigate (total depth > vessel draught)
    can_navigate = total_depths > vessel.draught

    # Convert can_navigate array into tidal windows
    tidal_windows = []
    window_start = None
    
    for i in range(len(can_navigate)):
        if can_navigate[i] and window_start is None:
            # Start of a new window
            window_start = time_range[i]
        elif not can_navigate[i] and window_start is not None:
            # End of a window
            tidal_windows.append((window_start, time_range[i-1]))
            window_start = None
    
    # Handle case where the last window ends at the last time point
    if window_start is not None:
        tidal_windows.append((window_start, time_range[-1]))
    
    return tidal_windows, time_range, total_depths


import matplotlib.pyplot as plt
from typing import List, Tuple

def plot_tidal_windows(tidal_windows: List[Tuple[pd.Timestamp, pd.Timestamp]], time_range: pd.DatetimeIndex, total_depths: List[float], vessel_draught: float, port_name: str):
    # Plotting
    plt.figure(figsize=(14, 7))
    plt.plot(time_range, total_depths, label='Total Depth (Harbor Depth + Tide)')
    plt.axhline(y=vessel_draught, color='r', linestyle='--', label=f'Vessel Draught ({vessel_draught} m)')
    
    # Highlight the tidal windows where navigation is possible
    for window_start, window_end in tidal_windows:
        plt.axvspan(window_start, window_end, color='green', alpha=0.3)
    
    plt.xlabel('Time')
    plt.ylabel('Water Depth (meters)')
    plt.title(f'Tidal Depths vs Vessel Draught at {port_name}')
    plt.legend()
    plt.show()
