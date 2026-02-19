import pandas as pd

class F1Predictor2026:
    def __init__(self):
        # Data based on final 2025 Standings and 2026 Grid confirmations
        self.drivers = {
            'Player': [
                'Lando Norris', 'Max Verstappen', 'Oscar Piastri', 'George Russell', 
                'Charles Leclerc', 'Lewis Hamilton', 'Kimi Antonelli', 'Alex Albon', 
                'Carlos Sainz', 'Fernando Alonso', 'Nico Hulkenberg', 'Isack Hadjar', 
                'Oliver Bearman', 'Liam Lawson', 'Esteban Ocon', 'Lance Stroll', 
                'Gabriel Bortoleto', 'Pierre Gasly', 'Franco Colapinto', 'Sergio Perez', 
                'Valtteri Bottas', 'Arvid Lindblad'
            ],
            'Debut': [2019, 2015, 2023, 2019, 2018, 2007, 2025, 2019, 2015, 2001, 2010, 2025, 2024, 2023, 2016, 2017, 2026, 2017, 2024, 2011, 2013, 2026],
            'Avg_Practice_25': [2.8, 3.1, 3.5, 4.2, 3.9, 5.5, 7.8, 9.1, 8.5, 9.5, 11.2, 10.5, 12.1, 13.5, 14.1, 15.2, 16.5, 14.8, 17.2, 12.5, 16.8, 18.0],
            'Avg_Quali_25': [2.9, 3.5, 3.0, 4.1, 4.8, 9.0, 8.5, 10.2, 9.8, 10.5, 11.5, 11.2, 12.5, 13.8, 14.5, 16.9, 15.8, 15.2, 16.9, 12.8, 16.5, 17.5],
            'Avg_Race_25': [2.4, 2.8, 3.1, 4.5, 3.9, 4.8, 6.2, 8.1, 7.5, 10.1, 11.2, 10.8, 12.4, 13.1, 14.2, 15.8, 15.5, 16.2, 17.5, 13.5, 16.9, 18.2],
            'Pit_ELO': [93, 94, 91, 90, 96, 92, 89, 84, 88, 95, 82, 86, 82, 85, 80, 75, 83, 79, 80, 78, 85, 81]
        }
        self.df = pd.DataFrame(self.drivers)

    def calculate_elo(self, current_year=2026):
        #  Experience ELO
        # Veterans get stability bonus, rookies get a potential baseline
        self.df['Exp_Years'] = current_year - self.df['Debut']
        self.df['Exp_Score'] = self.df['Exp_Years'] * 10 

        # Performance ELO 
        # Calculated from 2025 Speed (Practice + Quali)
        # invert the rank (23 - rank) so 1st place gets the highest points
        self.df['Speed_Rating'] = (23 - ((self.df['Avg_Practice_25'] + self.df['Avg_Quali_25']) / 2)) * 40
        
        # 3. Race & Pit ELO 
        # Only applies to Race day efficiency
        self.df['Race_Potential'] = (23 - self.df['Avg_Race_25']) * 35
        self.df['Pit_Bonus'] = self.df['Pit_ELO'] * 2

        # Final Weighted Prediction
        self.df['Win_Probability_Score'] = (
            (self.df['Exp_Score'] * 0.15) + 
            (self.df['Speed_Rating'] * 0.55) + 
            (self.df['Race_Potential'] * 0.20) + 
            (self.df['Pit_Bonus'] * 0.10)
        )
        
        return self.df.sort_values(by='Win_Probability_Score', ascending=False)

# Execution
if __name__ == "__main__":
    predictor = F1Predictor2026()
    results = predictor.calculate_elo()
    
    print("--- OFFICIAL F1 2026 ELO PREDICTIONS ---")
    print(results[['Player', 'Exp_Years', 'Win_Probability_Score']].head(10).to_string(index=False))
    
    winner = results.iloc[0]['Player']
    print(f"\nPredicted 2026 World Champion: {winner.upper()}")
