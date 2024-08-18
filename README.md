# Tidal and Daylight Window Forecasting API
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

Generating a Time Range: A time range covering the 14-day period from the vessel's arrival time is generated, with a resolution of 1 minute.

Interpolating Tidal Heights: The interpolation function is applied to this time range to generate a continuous series of tidal heights for every minute.

Calculating Total Depths: The interpolated tidal heights are added to the port's minimum water level to get the total water depth at each minute.

Identifying Navigable Windows: The total water depth is compared against the vessel's draught to identify time windows where the vessel can safely navigate.

Combined Tidal and Daylight Window Calculation
In addition to the tidal windows, the API also considers daylight restrictions at the port. The combined windows are calculated by intersecting the tidal windows with the daylight windows, ensuring that the vessel can navigate during daylight hours.