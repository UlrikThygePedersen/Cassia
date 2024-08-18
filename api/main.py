from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, condecimal
from datetime import datetime
from typing import List
from cassia.cassia import Cassia

# Initialize the Cassia class
cassia = Cassia()

app = FastAPI()

class VesselInfo(BaseModel):
    draught: condecimal(gt=0, decimal_places=2)
    dwt: condecimal(gt=0, decimal_places=2)
    name: str
    imo: int

class TidalWindowInput(BaseModel):
    port_id: str  # Assuming this is the UNLOCODE
    vessel_information: VesselInfo  # We expect one vessel per request here
    arrival_datetime: datetime

class TidalWindowOutput(BaseModel):
    start_time: datetime
    end_time: datetime

class TidalWindowResponse(BaseModel):
    tidal_windows: List[TidalWindowOutput]
    message: str = Field(default="Tidal window forecast generated successfully.")

@app.post("/tidal-windows/", response_model=TidalWindowResponse)
async def get_tidal_windows(input: TidalWindowInput):
    try:
        # Use the calculate_tidal_windows method from the cassia instance
        imo = input.vessel_information.imo
        unlocode = input.port_id
        arrival_time = input.arrival_datetime

        tidal_windows = cassia.get_tidal_windows(
            imo, unlocode, arrival_time
        )

        # Create the response list
        response_list = []
        for start_time, end_time in tidal_windows:
            response_list.append(TidalWindowOutput(
                start_time=start_time,
                end_time=end_time
            ))

        response = TidalWindowResponse(tidal_windows=response_list)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/combined-windows/", response_model=TidalWindowResponse)
async def get_combined_windows(input: TidalWindowInput):
    try:
        # Use the get_combined_windows method from the cassia instance
        imo = input.vessel_information.imo
        unlocode = input.port_id
        arrival_time = input.arrival_datetime

        combined_windows = cassia.get_combined_windows(
            imo, unlocode, arrival_time
        )

        # Create the response list
        response_list = []
        for start_time, end_time in combined_windows:
            response_list.append(TidalWindowOutput(
                start_time=start_time,
                end_time=end_time
            ))

        response = TidalWindowResponse(tidal_windows=response_list)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))