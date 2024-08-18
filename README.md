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

Combined Tidal and Daylight Window Calculation
In addition to the tidal windows, the API also considers daylight restrictions at the port. The combined windows are calculated by intersecting the tidal windows with the daylight windows, ensuring that the vessel can navigate during daylight hours.

API Endpoints
/tidal-windows/: Provides tidal windows for a given vessel and port.
/combined-windows/: Provides combined tidal and daylight windows for a given vessel and port.