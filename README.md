# Cassia - Tidal and Daylight Window Forecasting API

<img src="https://i.imgur.com/lYbRtT3.png" alt="cassia" width="900" height="420">


This repository provides a solution for predicting tidal windows and combined tidal-daylight windows for vessels arriving at a port. The API calculates the time windows when a vessel can safely navigate to the port, considering both tidal variations and daylight restrictions.

## Overview
### Purpose
The API is designed to help vessel operators determine the optimal time for vessels to enter a port and travel to a berth. It ensures safe navigation by accounting for both tidal variations and daylight availability, which are critical factors affecting a vessel's ability to enter the port.

### Key Features
* Tidal Window Calculation: Calculates the time windows when the water depth, considering tidal variations, is sufficient for a vessel to safely navigate to the port.
* Combined Window Calculation: Combines tidal windows with daylight restrictions to provide a comprehensive view of when the vessel can navigate safely.
* Visualization: Generates plots showing tidal variations, vessel draught, and the available navigation windows.
## How It Works
### Tidal Window Calculation
The tidal window calculation is based on the following inputs:

* Vessel Draught: The depth of water that the vessel occupies.
* Port's Minimum Water Level: The base water depth at the port.
* Tidal Forecast Data: Predicted tidal heights over time.
The API calculates when the water depth (port's minimum level + tidal height) exceeds the vessel's draught, indicating a safe navigation window.

### Interpolation of Tidal Data
The tidal heights provided in the forecast data are typically recorded at specific intervals (e.g., high and low tides). However, to accurately determine the water depth at any given minute over a 14-day period, interpolation is used.

Here's how interpolation is applied:

1. Data Preparation: The tidal data for the selected port is filtered and sorted by time. Each timestamp is converted into a numerical format (epoch time) for processing.

2. Linear Interpolation: The interp1d function from the scipy.interpolate module is used to create a continuous function that estimates the tidal height at any given time between the provided data points. Linear interpolation is chosen to maintain a balance between simplicity and accuracy.

3. Generating a Time Range: A time range covering the 14-day period from the vessel's arrival time is generated, with a resolution of 1 minute.

4. Interpolating Tidal Heights: The interpolation function is applied to this time range to generate a continuous series of tidal heights for every minute.

5. Calculating Total Depths: The interpolated tidal heights are added to the port's minimum water level to get the total water depth at each minute.

6. Identifying Navigable Windows: The total water depth is compared against the vessel's draught to identify time windows where the vessel can safely navigate.

### Combined Tidal and Daylight Window Calculation
In addition to the tidal windows, the API also considers daylight restrictions at the port. The combined windows are calculated by intersecting the tidal windows with the daylight windows, ensuring that the vessel can navigate during daylight hours.

## API Endpoints
* /tidal-windows/: Provides tidal windows for a given vessel and port.
* /combined-windows/: Provides combined tidal and daylight windows for a given vessel and port.
### Example Request
```json
{
  "port_id": "AUBNE",
  "vessel_information": {
    "draught": "14.45",
    "dwt": "80276.0",
    "name": "EPIPHANIA",
    "imo": 9582116
  },
  "arrival_datetime": "2024-03-01T00:00:00"
}
```
### Example Response
```json
{
  "tidal_windows": [
    {
      "start_time": "2024-03-01T08:33:58.513561",
      "end_time": "2024-03-01T20:06:01.436258"
    },
    {
      "start_time": "2024-03-02T08:33:12.418624",
      "end_time": "2024-03-02T20:06:22.864523"
    }
    // additional windows...
  ],
  "message": "Tidal window forecast generated successfully."
}
```
## Visualization
To help the business side understand how the calculation works, we've created visualizations that display:

* Tidal Variation: How the water depth changes over time due to tides.
* Vessel Draught: The constant depth that the vessel occupies.
* Tidal Windows: Time windows where the water depth is sufficient for safe navigation.
* Combined Tidal and Daylight Windows: Time windows where both tidal conditions and daylight allow for safe navigation.
### Example Scenario Visualization
An example scenario has been visualized and is available in the CassiaExample.ipynb notebook. The notebook includes:

* Plot of Tidal Variations: Shows the changing water depth at the port due to tidal activity.
* Overlay of Vessel Draught: Indicates the minimum water depth required for the vessel to navigate safely.
* Tidal Windows Highlighted: Green shaded regions represent the time windows where the vessel can safely navigate based on tidal conditions.
* Combined Tidal and Daylight Windows: Highlighted areas that show when both conditions are met.
### Code Examples of Visualizations

```python
# Example usage of Brisbane with 01/03 2024 with the Epiphania ship
arrival_time = pd.Timestamp('2024-03-01 00:00:00')
imo = 9582116  # "EPIPHANIA"
unlocode = 'AUBNE'  # Brisbane

cassia = Cassia()

tidal_windows = cassia.get_tidal_windows(
    imo=imo,
    unlocode=unlocode,
    arrival_time=arrival_time
)

cassia.plot_tidal_windows(
    imo=imo,
    unlocode=unlocode
)
```
![cassia](assets/cassia.png)

<img src="assets/cassia.png" alt="cassia" width="900" height="420">



## Conclusion
This API, along with the accompanying visualizations, provides a robust tool for predicting when a vessel can safely enter a port. By taking into account both tidal variations and daylight restrictions, the API ensures that vessel operators have the information they need to make safe and efficient decisions.

Feel free to explore the CassiaExample.ipynb notebook to see the calculations in action and understand how the navigation windows are determined.