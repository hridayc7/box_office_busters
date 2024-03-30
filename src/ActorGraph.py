import pandas as pd
import json
from CastInfo import CastInfo
from ComputeROI import ComputeROI
from typing import Optional
import igraph as ig
from collections import defaultdict
import numpy as np

class ActorGraph():
    def __init__(self):
        cast = CastInfo()
        # set: {<actor_name1>,...,<actor_nameN>}
        self.ACTORS = cast.load_unique_actors_from_file('../data/tmdb/all_actors.txt')
        # dict: {<actor_id>:<actor_name>}
        self.ACTOR_IDS = self.open_json('../data/tmdb/actor_ids.json')
        # dict {tmdb_id: List[<actor_id1>, <actor_id2>, <actor_id3>]}
        self.ACTORS_BY_MOVIE = self.name_to_id(cast.load_movie_actors_from_json('../data/tmdb/top_five_actors_by_movie.json'))
        self.TMDB_INFO = pd.read_csv('../data/tmdb/combined_tmdb_data.csv')
        self.roi = ComputeROI()
        # dict: {tmdb_id:roi}
        self.ALL_ROI = self.roi.compute_all_roi()
    
    def open_json(self, file_path:str) -> dict:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

    def name_to_id(self, dict_in:dict) -> dict:
        name_to_id = {name: actor_id for actor_id, name in self.ACTOR_IDS.items()}
        updated_actors_by_movie = {}
        for movie_id, actors in dict_in.items():
            updated_actor_ids = [name_to_id[actor_name] for actor_name in actors if actor_name in name_to_id]
            updated_actors_by_movie[movie_id] = updated_actor_ids
        return updated_actors_by_movie

    def build_graph(self):
        # G = (V,E)
        # V = actor IDs
        # E = (tmdb_id, release_year, roi)
        pass
    

    
ag = ActorGraph()
#print(ag.ACTORS_BY_MOVIE)
print(ag.ALL_ROI)