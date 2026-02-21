🏎️ F1 Predictions & ELO Model (2025-2026)
Welcome to the f1-ml-project repository! This project combines Machine Learning (Gradient Boosting) and a custom ELO Rating System to predict race outcomes and driver rankings for the 2025 and 2026 Formula 1 seasons.

🚀 Project Overview
This repository features a dual-approach to F1 analytics:

ML Predictions: A Gradient Boosting model that uses FastF1 telemetry and historical data to predict lap times and race winners for 2025.

ELO Ranking: A specialized 2026 ELO model that calculates driver "Quickness" by isolating Practice/Qualifying speed from Race-day pit efficiency.

📊 Data & Methodology
We leverage the FastF1 API to pull high-fidelity data, including:

Historical Results: 2024–2025 race and qualifying data for model training.

Telemetry: Lap times and sector speeds to refine the Gradient Boosting Regressor.

Debut Year Data: Used in the ELO model to calculate "Experience Points" for veterans vs. rookies.

🏁 How It Works
1. The Machine Learning Pipeline (prediction1.py, prediction2.py)
Preprocessing: Normalizes driver names and lap times.

Training: Uses a Gradient Boosting Regressor trained on previous season benchmarks.

Evaluation: Performance is measured using Mean Absolute Error (MAE) to ensure accuracy within seconds of actual race times.

2. The 2026 ELO Predictor (Predictor-2026-ELO.py)
This follows a specific logic to determine the "Quickest Overall" driver:

Speed ELO: Calculated strictly from Friday Practice and Saturday Sorting (Qualifying).

Race/Pit ELO: Pit stop reaction times are factored in only during the race calculation phase to avoid skewing raw speed data.

Longevity Factor: Rewards drivers based on their career start date (e.g., Fernando Alonso's 2001 debut vs. Arvid Lindblad's 2026 debut).

🗂️ Repository Structure
prediction1.py - Initial ML model for the 2025 Australian GP.

prediction2.py - Updated pipeline for mid-season 2025 adjustments.

Predictor-2026-ELO.py - The advanced ELO engine for the 2026 season.

requirements.txt - Project dependencies (FastF1, Pandas, Scikit-learn).

🔧 Usage
To run the latest 2026 ELO prediction:

Bash
python3 Predictor-2026-ELO.py
To run a specific race prediction:

Bash
python3 prediction1.py
📈 Expected Output
Plaintext
🏁 Predicted 2026 ELO Standings 🏁
1. Max Verstappen - ELO: 2021 (Grandmaster)
2. Lando Norris   - ELO: 1985 (Grandmaster)
...
🔍 Model Error (MAE): 3.22 seconds
📌 Future Goals
Integrate FastAPI to serve these predictions as a live web service.

Incorporate Weather Conditions (Live API) to adjust ELO for wet-weather specialists.
