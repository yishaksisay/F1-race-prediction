import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor

# DRIVER
drivers = pd.DataFrame({
    "Driver":[
        "Verstappen","Perez","Hamilton","Russell","Leclerc",
        "Sainz","Norris","Piastri","Alonso","Stroll",
        "Gasly","Ocon","Tsunoda","Ricciardo","Albon",
        "Sargeant","Bottas","Zhou","Magnussen","Hulkenberg"
    ],
    "YearsF1":[9,13,17,6,7,10,6,2,22,8,7,8,4,13,5,2,12,3,9,13],
    "AvgRaceFinish":[2.3,6.5,4.1,5.3,3.9,4.8,3.6,4.2,5.1,9.8,7.3,8.2,9.5,8.9,7.7,12.5,9.0,10.8,11.2,10.1],
    "AvgQuali":[2.1,7.0,4.5,5.0,3.5,4.2,3.1,3.9,6.2,10.5,8.5,8.9,10.2,9.1,8.0,13.0,10.0,11.5,12.2,11.0],
    "RacePace":[90.1,91.8,90.9,91.0,90.5,90.7,90.4,90.6,91.1,92.0,91.5,91.6,92.2,91.7,91.3,93.0,92.0,92.5,92.7,92.3],
    "TrackStarts":[7,8,15,5,6,9,5,1,18,6,5,6,3,8,4,1,10,2,7,10],
    "TrackAvgFinish":[2.0,5.8,3.5,6.0,3.0,4.2,4.0,5.0,4.8,9.5,7.0,8.5,9.2,8.7,7.2,12.0,9.5,10.3,11.1,10.0]
})

# ELO SCORE
drivers["ELO"] = (
    drivers["YearsF1"] * 8 * 0.20 +
    (20 - drivers["AvgQuali"]) * 25 * 0.30 +
    (20 - drivers["AvgRaceFinish"]) * 30 * 0.35 +
    (20 - drivers["TrackAvgFinish"]) * 20 * 0.15
)


# ML MODEL

features = [
    "ELO",
    "AvgQuali",
    "AvgRaceFinish",
    "RacePace",
    "TrackStarts",
    "TrackAvgFinish"
]

X = drivers[features]
y = drivers["RacePace"] * 0.97 + drivers["AvgRaceFinish"] * 0.4

model = GradientBoostingRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=3,
    random_state=42
)

model.fit(X, y)

drivers["PredictedScore"] = model.predict(X)

# FINAL RANKING

ranking = drivers.sort_values("PredictedScore").reset_index(drop=True)
ranking["Position"] = ranking.index + 1

print("\ RACE PREDICTIONn")
print(ranking[["Position","Driver","ELO","PredictedScore"]])
