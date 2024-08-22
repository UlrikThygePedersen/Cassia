import pytest
import pandas as pd # type:ignore
from cassia.cassia import Cassia



@pytest.mark.parametrize("vessel_imo", [9790933, 9331866, 9251315, 9494008, 9461128, 9473121, 9582116, 9991234, 9758571, 9591765])
@pytest.mark.parametrize("unlocode", ['AUBNE', 'AUABP', 'AUDAM', 'AUCTN'])
def test_cassia_tidal_windows(cassia_instance, load_vessels, load_ports, vessel_imo, unlocode):
    """Test tidal windows calculation for different vessels and ports."""

    # Extract vessel information from loaded DataFrame
    vessel = load_vessels.loc[load_vessels['IMO'] == vessel_imo].iloc[0]
    
    arrival_time = pd.Timestamp('2024-03-01 00:00:00')
    
    tidal_windows, time_range, total_depths = cassia_instance.get_tidal_windows(
        imo=vessel['IMO'],
        unlocode=unlocode,
        arrival_time=arrival_time
    )

    assert isinstance(tidal_windows, list), "Tidal windows should be a list."
    assert all(isinstance(window, tuple) for window in tidal_windows), "Each window should be a tuple."
    assert all(len(window) == 2 for window in tidal_windows), "Each window tuple should contain start and end times."
    assert len(tidal_windows) > 0, f"No tidal windows found for vessel {vessel['NAME']} at port {unlocode}."



# Vessels likely to find a window
vessels_with_windows = [
    {"imo": 9790933, "draught": 13.418, "name": "UNITY LIFE"},      # All ports
    {"imo": 9331866, "draught": 12.573, "name": "MING HUA"},        # All ports
    {"imo": 9251315, "draught": 12.020, "name": "VIVA GLOBUS"},     # All ports
    {"imo": 9494008, "draught": 14.430, "name": "VELSHEDA"},        # AUABP, AUDAM
    {"imo": 9461128, "draught": 14.429, "name": "NEA TYHI"},        # AUABP, AUDAM
    {"imo": 9473121, "draught": 14.210, "name": "NIKOLAOS"},        # All ports
]

# Vessels likely NOT to find a window
vessels_without_windows = [
    {"imo": 9991234, "draught": 36.800, "name": "JIMMY T"},         # All ports
    {"imo": 9582116, "draught": 14.450, "name": "EPIPHANIA"},       # AUBNE, AUCTN, AUDAM
    {"imo": 9758571, "draught": 14.450, "name": "HUA SHENG HAI"},   # AUBNE, AUCTN, AUDAM
    {"imo": 9591765, "draught": 14.900, "name": "MBA ROSARIA"}      # AUBNE, AUCTN, AUDAM
]

# Ports
ports = ['AUBNE', 'AUABP', 'AUDAM', 'AUCTN']

# Test Vessels That Should Find a Window
@pytest.mark.parametrize("vessel", vessels_with_windows)
@pytest.mark.parametrize("unlocode", ports)
def test_vessels_with_windows(cassia_instance, load_vessels, load_ports, vessel, unlocode):
    """Test vessels that should find a tidal window."""
    arrival_time = pd.Timestamp('2024-03-01 00:00:00')
    
    tidal_windows, time_range, total_depths = cassia_instance.get_tidal_windows(
        imo=vessel['imo'],
        unlocode=unlocode,
        arrival_time=arrival_time
    )

    # Ensure tidal windows are found
    assert len(tidal_windows) > 0, f"No tidal windows found for vessel {vessel['name']} at port {unlocode}."


# Test Vessels That Should NOT Find a Window
@pytest.mark.parametrize("vessel", vessels_without_windows)
@pytest.mark.parametrize("unlocode", ports)
def test_vessels_without_windows(cassia_instance, load_vessels, load_ports, vessel, unlocode):
    """Test vessels that should not find a tidal window."""
    arrival_time = pd.Timestamp('2024-03-01 00:00:00')
    
    tidal_windows, time_range, total_depths = cassia_instance.get_tidal_windows(
        imo=vessel['imo'],
        unlocode=unlocode,
        arrival_time=arrival_time
    )

    # Ensure no tidal windows are found if the draught is too deep for the port
    if vessel['draught'] >= load_ports.loc[load_ports['UNLOCODE'] == unlocode]['APPROACH_MLLW_METERS'].values[0]:
        assert len(tidal_windows) == 0, f"Tidal windows should not be available for vessel {vessel['name']} at port {unlocode}."
    else:
        assert len(tidal_windows) > 0, f"Tidal windows should be available for vessel {vessel['name']} at port {unlocode}."
