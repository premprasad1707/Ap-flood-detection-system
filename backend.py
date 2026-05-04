import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pandas as pd
import json

from utils.model import calculate_risk, classify_risk
from utils.geo_utils import load_shapefiles, load_rainfall_data

app = FastAPI(title="FloodSense API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data at startup
canals, embankments = load_shapefiles()
rainfall_df = load_rainfall_data()

class PredictRequest(BaseModel):
    rainfall: float
    prev_rainfall: float
    elevation: float
    slope: float

@app.get("/")
def serve_frontend():
    return FileResponse("index.html")

@app.get("/api/locations")
def get_locations():
    if rainfall_df is not None and not rainfall_df.empty and 'location' in rainfall_df.columns:
        locations = sorted(rainfall_df['location'].unique().tolist())
        return {"locations": locations}
    return {"locations": []}

@app.get("/api/location/{loc_name}")
def get_location_data(loc_name: str):
    if rainfall_df is not None and not rainfall_df.empty and 'location' in rainfall_df.columns:
        matches = rainfall_df[rainfall_df['location'] == loc_name]
        if not matches.empty:
            loc_data = matches.iloc[0]
            return {
                "latitude": float(loc_data['latitude']),
                "longitude": float(loc_data['longitude']),
                "rainfall": max(0.0, float(loc_data['rainfall'])),
                "prev_rainfall": max(0.0, float(loc_data['prev_rainfall']))
            }
    raise HTTPException(status_code=404, detail="Location not found")

@app.post("/api/predict")
def predict_risk(req: PredictRequest):
    score = calculate_risk(req.rainfall, req.prev_rainfall, req.elevation, req.slope)
    level = classify_risk(score)
    return {
        "score": score,
        "level": level
    }

@app.get("/api/map/canals")
def get_canals():
    if canals is not None:
        return json.loads(canals.to_json())
    return {}

@app.get("/api/map/embankments")
def get_embankments():
    if embankments is not None:
        return json.loads(embankments.to_json())
    return {}

if __name__ == "__main__":
    uvicorn.run("backend:app", host="0.0.0.0", port=8000, reload=True)
