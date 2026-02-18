import fastf1
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingRegressor

class F1_Global_Predictor_2025:

    def __init__(self):
        fastf1.Cache.enable_cache("f1_cache")
        self.model = GradientBoostingRegressor(n_estimators=300, learning_rate=0.08, random_state=42)

    def get_driver_database(self):
        # The complete 2025 Grid with Full Names and Qualifying Data
        grid_2025 = pd.DataFrame({
            'FullName': [
                'Lando Norris', 'Oscar Piastri', 'Max Verstappen', 'Liam Lawson',
                'Charles Leclerc', 'Lewis Hamilton', 'George Russell', 'Andrea Kimi Antonelli',
                'Fernando Alonso', 'Lance Stroll', 'Carlos Sainz Jr.', 'Alexander Albon',
                'Pierre Gasly', 'Jack Doohan', 'Esteban Ocon', 'Oliver Bearman',
                'Nico Hulkenberg', 'Gabriel Bortoleto', 'Yuki Tsunoda', 'Isack Hadjar'
            ],
            'Code': [
                'NOR', 'PIA', 'VER', 'LAW', 'LEC', 'HAM', 'RUS', 'ANT', 
                'ALO', 'STR', 'SAI', 'ALB', 'GAS', 'DOO', 'OCO', 'BEA', 
                'HUL', 'BOR', 'TSU', 'HAD'
            ],
            'QualiTime': [
                75.096, 75.180, 75.481, 75.900, 75.755, 75.973, 75.546, 76.410,
                75.800, 76.350, 76.062, 75.737, 75.980, 76.800, 76.200, 76.900,
                76.100, 77.050, 75.670, 77.200
            ]
        })
        return grid_2025

    def train_on_history(self):
        print("2024 Telemetry for baseline training")
        # Training on Australia 2024 to find the Quali-to-Race Pace ratio
        session = fastf1.get_session(2024, 'Australia', 'R')
        session.load()
        laps = session.laps[['Driver', 'LapTime']].dropna()
        laps['Seconds'] = laps['LapTime'].dt.total_seconds()
        return laps.groupby('Driver')['Seconds'].mean().to_dict()

    def run_simulation(self):
        grid = self.get_driver_database()
        history = self.train_on_history()
        
        # Merge logic
        grid['HistoricalPace'] = grid['Code'].map(history).fillna(np.mean(list(history.values())))
        
        #  Quali Speed + Experience Pace
        X = grid[['QualiTime', 'HistoricalPace']]
        y = grid['HistoricalPace'] * 0.975 # 2025 cars roughly 2.5% faster
        
        self.model.fit(X, y)
        grid['PredictedPace'] = self.model.predict(X)
        return grid.sort_values('PredictedPace').reset_index(drop=True)

    def plot_beautiful_results(self, results):
        plt.style.use('dark_background')
        plt.figure(figsize=(14, 8))
        
        # Color mapping for the podium
        colors = ['#FFD700', '#C0C0C0', '#CD7F32'] + ['#1e3799'] * (len(results) - 3)
        
        plt.barh(results['FullName'], results['PredictedPace'], color=colors)
        plt.xlabel('Predicted Lap Time', fontsize=12, color='white')
        plt.title('2025 AUSTRALIAN GP: PREDICTION ', fontsize=16, fontweight='bold')
        plt.gca().invert_yaxis()
        plt.grid(axis='x', linestyle='--', alpha=0.3)
        plt.show()

#  THE TEST 
if __name__ == "__main__":
    engine = F1_Global_Predictor_2025()
    final_results = engine.run_simulation()
    
    print("\n" + "═"*60)
    print(" 2025 PREDICTION REPORT")
    print("═"*60)
    print(final_results[['FullName', 'PredictedPace']].to_string(index=False))
    print("═"*60)
    
    engine.plot_beautiful_results(final_results)
