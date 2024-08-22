from dataclasses import dataclass

import pandas as pd  # type: ignore

from pathlib import Path


current_dir = Path(__file__).resolve().parent

vessels_csv_path = current_dir / "../assets/vessels.csv"
ports_csv_path = current_dir / "../assets/ports.csv"
vessel_df = pd.read_csv(vessels_csv_path.resolve())
port_df = pd.read_csv(ports_csv_path.resolve())


@dataclass
class Vessel:
    imo: int
    draught: float
    name: str
    dwt: float


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


ports_dispatcher = {
    row["UNLOCODE"]: Port(
        name=row["NAME"],
        latitude=row["LATITUDE"],
        longitude=row["LONGITUDE"],
        approach_mllw_meters=row["APPROACH_MLLW_METERS"],
    )
    for _, row in port_df.iterrows()
}
