from dataclasses import dataclass

import pandas as pd # type: ignore


@dataclass
class Vessel:
    imo: int
    draught: float
    name: str
    dwt: float

vessel_df = pd.read_csv("../assets/vessels.csv")

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



port_df = pd.read_csv("../assets/ports.csv")

# create dispatcher for access to ports based on their UNLOCODE
ports_dispatcher = {
    row['UNLOCODE']: Port(
        name=row['NAME'],
        latitude=row['LATITUDE'],
        longitude=row['LONGITUDE'],
        approach_mllw_meters=row['APPROACH_MLLW_METERS']
    )
    for _, row in port_df.iterrows()
}
