from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(title="F1 2026 Performance Predictor", description="ELO-based ranking system for the 2026 Grid")

            # Player
class DriverPerformance(BaseModel):
    name: str
    debut_year: int
    avg_practice_25: float
    avg_quali_25: float
    avg_race_25: float
    pit_stop_elo: float 
    
    # Only for Race Calculati
         #  DATABASE
# Based on 2025 results
db = [
    {"name": "Lando Norris", "debut_year": 2019, "avg_practice_25": 2.8, "avg_quali_25": 2.9, "avg_race_25": 2.4, "pit_stop_elo": 1850},
    {"name": "Max Verstappen", "debut_year": 2015, "avg_practice_25": 3.1, "avg_quali_25": 3.5, "avg_race_25": 2.8, "pit_stop_elo": 1870},
    {"name": "Charles Leclerc", "debut_year": 2018, "avg_practice_25": 3.9, "avg_quali_25": 4.8, "avg_race_25": 3.9, "pit_stop_elo": 1950},
    {"name": "Lewis Hamilton", "debut_year": 2007, "avg_practice_25": 5.5, "avg_quali_25": 9.0, "avg_race_25": 4.8, "pit_stop_elo": 1920},
    {"name": "Kimi Antonelli", "debut_year": 2025, "avg_practice_25": 7.8, "avg_quali_25": 8.5, "avg_race_25": 6.2, "pit_stop_elo": 1750}
]

# THE ELO
def calculate_2026_elo(driver):
    #  Pace - No Pits
    speed_factor = (23 - ((driver['avg_practice_25'] + driver['avg_quali_25']) / 2)) * 10
    
    # Race Finish + Pit Reaction
    # Pit stops affect this also
    race_factor = (23 - driver['avg_race_25']) * 8
    pit_factor = (driver['pit_stop_elo'] / 100) * 5
    
    # Years played
    experience_factor = (2026 - driver['debut_year']) * 2
    
    return round(speed_factor + race_factor + pit_factor + experience_factor, 2)

#  API
@app.get("/")
async def root():
    return {"status": "Pit Wall Online", "season": 2026}

@app.get("/rankings")
async def get_rankings():
    """Returns the full 2026 Predicted Standings from Top to Lowest ELO."""
    scored_list = []
    for d in db:
        score = calculate_2026_elo(d)
        scored_list.append({"player": d['name'], "elo_2026": score})
    
    # Sorting highest  to lowest    elo
    return sorted(scored_list, key=lambda x: x['elo_2026'], reverse=True)

@app.get("/predict/{driver_name}")
async def predict_driver(driver_name: str):
    """Deep dive into a specific driver's 2026 potential."""
    driver = next((item for item in db if item["name"].lower() == driver_name.lower()), None)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found in 2026 grid")
    
    return {
        "driver": driver['name'],
        "total_elo": calculate_2026_elo(driver),
        "tier": "Grandmaster" if calculate_2026_elo(driver) > 400 else "Challenger"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
