import pandas as pd
import json
from CastInfo import CastInfo
from ComputeROI import ComputeROI
from typing import Optional
import igraph as ig
from collections import defaultdict
import numpy as np
import csv
from tqdm import tqdm
class ActorGraph():
    def __init__(self):
        cast = CastInfo()
        # set: {<actor_name1>,...,<actor_nameN>}
        self.ACTORS = cast.load_unique_actors_from_file('../data/tmdb/all_actors.txt')
        # dict: {<actor_id>:<actor_name>}
        self.ACTOR_IDS = self.open_json('../data/tmdb/actor_ids.json')
        # dict {tmdb_id: List[<actor_id1>, <actor_id2>, <actor_id3>]}
        self.ACTORS_BY_MOVIE = self.name_to_id(cast.load_movie_actors_from_json('../data/tmdb/top_three_actors_by_movie.json'))
        self.TMDB_INFO = pd.read_csv('../data/tmdb/combined_tmdb_data.csv')
        self.roi = ComputeROI()
        # dict: {tmdb_id:roi}
        self.ALL_ROI = self.roi.compute_all_roi()
        self.graph = self.build_graph()
    
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

        g = ig.Graph(directed=False)
        g.add_vertices(list(self.ACTOR_IDS.keys()))
        
        for movie_id, actors in tqdm(self.ACTORS_BY_MOVIE.items()):
            release_date = self.TMDB_INFO.loc[self.TMDB_INFO['id'] == int(movie_id), 'release_date'].values[0]
            release_year = int(release_date.split('-')[0]) if isinstance(release_date, str) else None
            roi = self.ALL_ROI[int(movie_id)]
            
            for i in range(len(actors)):
                for j in range(i + 1, len(actors)):
                    actor_a, actor_b = actors[i], actors[j]
                    if not g.are_connected(actor_a, actor_b):
                        # Initialize edge attribute as a dictionary with year as key and ROI as value
                        g.add_edge(actor_a, actor_b, roi={release_year: (roi,1)} if roi is not None else {})
                    else:
                        edge_id = g.get_eid(actor_a, actor_b)
                        edge_data = g.es[edge_id].attributes()
                        # Update the ROI for the year, or add a new year if not present
                        if release_year in edge_data['roi']:
                            if roi is not None:
                                # Update total ROI and count
                                total_roi, count = edge_data['roi'][release_year]
                                edge_data['roi'][release_year] = (total_roi + roi, count + 1)
                        else:
                            edge_data['roi'][release_year] = (roi, 1) if roi is not None else (0, 0)
                        g.es[edge_id].update_attributes(edge_data)
        
        for edge in g.es:
            edge_data = edge.attributes()
            avg_roi = {year: total_roi / count for year, (total_roi, count) in edge_data['roi'].items()}
            edge.update_attributes(roi=avg_roi)

        return g
    
    def write_graph_to_csv(self,  file_path):
        edge_data = []
        for edge in self.graph.es:
            source_actor = self.graph.vs[edge.source]['name']
            target_actor = self.graph.vs[edge.target]['name']
            roi_dict = edge['roi']

            # Iterate through the years in the ROI dictionary
            for year, roi in roi_dict.items():
                # Append the edge data to the list
                edge_data.append({
                    'source_actor': source_actor,
                    'target_actor': target_actor,
                    'year': year,
                    'roi': roi
                })

        # Convert the list of edge data to a DataFrame
        edge_df = pd.DataFrame(edge_data)

        # Write the DataFrame to a CSV file
        edge_df.to_csv(file_path, index=False)

ag = ActorGraph()
output_file_path = '../src/actor_graph.csv'
ag.write_graph_to_csv(output_file_path)
#print(ag.ACTORS_BY_MOVIE)
#print(ag.ALL_ROI)