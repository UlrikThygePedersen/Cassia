import pytest
import pandas as pd  # type:ignore
from hypothesis import given, strategies as st
from hypothesis.extra.pandas import column, data_frames


# Hypothesis test: Validate tidal windows based on port MLLW and vessel draught
@given(
    vessel_imo=st.sampled_from(
        [
            9790933,
            9331866,
            9251315,
            9494008,
            9461128,
            9473121,
            9582116,
            9991234,
            9758571,
            9591765,
        ]
    ),
    unlocode=st.sampled_from(["AUBNE", "AUABP", "AUDAM", "AUCTN"]),
    draught=st.floats(min_value=5.0, max_value=40.0),
    arrival_time=st.datetimes(
        min_value=pd.Timestamp("2024-01-01"), max_value=pd.Timestamp("2024-12-31")
    ),
)
def test_tidal_windows_with_hypothesis(
    cassia_instance,
    load_ports,
    load_vessels,
    vessel_imo,
    unlocode,
    draught,
    arrival_time,
):
    """Test tidal windows calculation using Hypothesis for property-based testing."""

    port_mllw = load_ports.loc[load_ports["UNLOCODE"] == unlocode][
        "APPROACH_MLLW_METERS"
    ].values[0]

    load_vessels.loc[load_vessels["IMO"] == vessel_imo, "DRAUGHT"] = draught

    tidal_windows, time_range, total_depths = cassia_instance.get_tidal_windows(
        imo=vessel_imo, unlocode=unlocode, arrival_time=pd.Timestamp(arrival_time)
    )

    if draught >= port_mllw:
        assert (
            len(tidal_windows) == 0
        ), f"Unexpected tidal windows for draught {draught} and port {unlocode}."
    else:
        assert (
            len(tidal_windows) > 0
        ), f"No tidal windows found for draught {draught} and port {unlocode}."


# Hypothesis test: Generate arbitrary DataFrames to simulate different vessel and port configurations
@given(
    vessels_df=data_frames(
        columns=[
            column("IMO", st.integers(min_value=9000000, max_value=9999999)),
            column("DRAUGHT", st.floats(min_value=5.0, max_value=40.0)),
            column("NAME", st.text()),
            column("DWT", st.floats(min_value=1000.0, max_value=100000.0)),
        ]
    ),
    ports_df=data_frames(
        columns=[
            column("UNLOCODE", st.sampled_from(["AUBNE", "AUABP", "AUDAM", "AUCTN"])),
            column("APPROACH_MLLW_METERS", st.floats(min_value=5.0, max_value=20.0)),
            column("NAME", st.text()),
            column("LATITUDE", st.floats(min_value=-90.0, max_value=90.0)),
            column("LONGITUDE", st.floats(min_value=-180.0, max_value=180.0)),
        ]
    ),
)
def test_tidal_windows_with_arbitrary_data(cassia_instance, vessels_df, ports_df):
    """Test tidal windows using Hypothesis-generated DataFrames."""

    for index, vessel in vessels_df.iterrows():
        for index, port in ports_df.iterrows():
            tidal_windows, time_range, total_depths = cassia_instance.get_tidal_windows(
                imo=vessel["IMO"],
                unlocode=port["UNLOCODE"],
                arrival_time=pd.Timestamp("2024-03-01 00:00:00"),
            )

            if vessel["DRAUGHT"] >= port["APPROACH_MLLW_METERS"]:
                assert (
                    len(tidal_windows) == 0
                ), f"Unexpected tidal windows for vessel {vessel['NAME']} and port {port['UNLOCODE']}."
            else:
                assert (
                    len(tidal_windows) > 0
                ), f"No tidal windows found for vessel {vessel['NAME']} and port {port['UNLOCODE']}."
