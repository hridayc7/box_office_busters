import pandas as pd
from typing import Optional, Dict

class ComputeROI():
    def __init__(self):
        self.TMDB_INFO = pd.read_csv('../data/tmdb/combined_tmdb_data.csv')

    def get_movie_name_by_id(self, tmdb_id:int) -> Optional[str]:
        name = self.TMDB_INFO[self.TMDB_INFO['id'] == tmdb_id]
        if not name.empty:
            return name.iloc[0]['title']
        else:
            print(f'No movie found for \'{tmdb_id}\'')
            return None

    def compute_individual_roi(self, tmdb_id: int) -> float:
        # Ensure 'id' column is treated as integer for comparison
        self.TMDB_INFO['id'] = self.TMDB_INFO['id'].astype(int)
        
        movie_row = self.TMDB_INFO.loc[self.TMDB_INFO['id'] == tmdb_id]
        if not movie_row.empty:
            movie_name = movie_row['title'].values[0]
            budget = movie_row['budget'].values[0]
            revenue = movie_row['revenue'].values[0]
            
            # Calculate ROI
            roi = (revenue - budget) / budget if budget else float('inf')  # Avoid division by zero
            print(f'Movie name: {movie_name}')
            print(f'Budget:  {budget}')
            print(f'Revenue: {revenue}')
            print(f'ROI:     {roi}')
            return roi
        else:
            print(f'No movie found for \'{tmdb_id}\'')
            return None
        
    def compute_all_roi(self) -> Dict[int, float]:
        roi_dict = {}
        # Ensure 'id' column is treated as integer for comparison
        self.TMDB_INFO['id'] = self.TMDB_INFO['id'].astype(int)
        for index, row in self.TMDB_INFO.iterrows():
            tmdb_id = row['id']
            budget = row['budget']
            revenue = row['revenue']
            # Calculate ROI and handle division by zero
            roi = (revenue - budget) / budget if budget else float('inf')
            roi_dict[tmdb_id] = roi
        return roi_dict