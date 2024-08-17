from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, condecimal
from datetime import datetime
from typing import List

app = FastAPI()

class TidalWindowInput(BaseModel):
    port_id: int
    vessel_draught: condecimal(gt=0, decimal_places=2)
    arrival_datetime: datetime

class TidalWindowOutput(BaseModel):
    start_time: datetime
    end_time: datetime
    can_navigate: bool

class TidalWindowResponse(BaseModel):
    tidal_windows: List[TidalWindowOutput]
    message: str = Field(default="Tidal window forecast generated successfully.")

# Heartbeat endpoint
@app.get("/heartbeat")
def heartbeat():
    return {"status": "I am alive :)"}

# Predict endpoint - Tidal Window
@app.post("/tidal-windows/", response_model=TidalWindowResponse)
async def get_tidal_windows(input: TidalWindowInput):
    try:
        # Use the calculate_tidal_windows function from the cassia module
        tidal_windows = calculate_tidal_windows(input.port_id, float(input.vessel_draught), str(input.arrival_datetime))
        response = TidalWindowResponse(tidal_windows=tidal_windows)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# New endpoint - Tidal and Daylight Window Combined
@app.post("/combined-windows/", response_model=TidalWindowResponse)
async def get_combined_windows(input: TidalWindowInput):
    try:
        # Use the calculate_combined_windows function from the cassia module
        combined_windows = calculate_combined_windows(input.port_id, float(input.vessel_draught), str(input.arrival_datetime))
        response = TidalWindowResponse(tidal_windows=combined_windows)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))