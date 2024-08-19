# Forecast tidal window
When can my vessel enter the port and travel until the berth?

Problem
Part 1
Consider the scenario of a marine vessel which is entering a port area and attempting to navigate to a safe berth, in order to load or discharge its cargo.

At any time, a vessel will have a certain draught - the depth that the vessel is sitting in the water. Laden vessels will often have such a deep draught that, until they can reach a berth and begin to discharge their cargo, they will only be able to navigate safely at high tide. In other words, the port area will have a baseline water depth, and the height of the tide is added to this baseline to give the total water depth at any given time.

Your task is to create a feature that will help a vessel operator know precisely when their vessel will be affected by tidal restrictions on arrival to the port. This feature should be in the form of a Python API. This API should accept the following request parameters:

The arrival port identifier
The vessel characteristics
The date and time of arrival
In response, the API should return all the tidal windows for the next 14 days from the arrival time. That is, it should contain all the information needed to classify any time in the next 14 days from the arrival time as "in" or "out" of a tide window.

Note: The tide data is already a forecast and is available for 14+ days ahead. In other words, you do not need to predict the tides - just use the tide forecast and the draught information to construct the tidal windows.

Data
The dataset tide_heights.csv contains, for several distinct ports, the highest and lowest points of each tide - it is up to you how to interpolate between these high and low points.

In addition, you are provided with two other datasets: ports.csv, which contains information about each port in your tide dataset, and vessels.csv, which gives a list of example vessels to help you test your code.

Part 2
In addition to tidal restrictions, some ports also restrict passage through the port area during nighttime, due to the reduced visibility of potential hazards. In order for a vessel to be permitted to go to the berth, it needs to comply with both tidal and daylight restrictions.

This time you are invited to find your own source of daylight information for each port, and create a second API which now returns the overall restriction windows for the next 14 days from the arrival time - combining both tidal and daylight restrictions.

Part 3
You've created the API - now to explain to the business side how the calculation works. Produce one or more charts with an example scenario of an arriving vessel to a port - displaying the tidal variation, the draught of the vessel, and the tidal or overall restrictions window clearly evident from the chart. The choice of visualization tool is up to you.