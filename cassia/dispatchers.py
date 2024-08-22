from dataclasses import dataclass

import pandas as pd  # type: ignore

from pathlib import Path

# Get the path of the current file (dispatchers.py) using pathlib
current_dir = Path(__file__).resolve().parent

# Construct the paths to the CSV files
vessels_csv_path = current_dir / '../assets/vessels.csv'
ports_csv_path = current_dir / '../assets/ports.csv'

@dataclass
class Vessel:
    imo: int
    draught: float
    name: str
    dwt: float


# Read the CSV files using the resolved paths
vessel_df = pd.read_csv(vessels_csv_path.resolve())

# create dispatcher for easy access to info about the vessel based on IMO unique identifier
vessels_dispatcher = {
    row["IMO"]: Vessel(
        imo=row["IMO"], draught=row["DRAUGHT"], name=row["NAME"], dwt=row["DWT"]
    )
    for _, row in vessel_df.iterrows()
}


@dataclass
class Port:
    name: str
    latitude: float
    longitude: float
    approach_mllw_meters: float


# Read the ports CSV file
port_df = pd.read_csv(ports_csv_path.resolve())

# create dispatcher for access to ports based on their UNLOCODE
ports_dispatcher = {
    row["UNLOCODE"]: Port(
        name=row["NAME"],
        latitude=row["LATITUDE"],
        longitude=row["LONGITUDE"],
        approach_mllw_meters=row["APPROACH_MLLW_METERS"],
    )
    for _, row in port_df.iterrows()
}
