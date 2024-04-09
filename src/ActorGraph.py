import pandas as pd
import json
from CastInfo import CastInfo
from ComputeROI import ComputeROI
from typing import Optional
import igraph as ig
from collections import defaultdict
import numpy as np
import networkx as nx
from networkx import MultiGraph
from itertools import combinations

class ActorGraph():
    def __init__(self):
        cast = CastInfo()
        # dict: {<actor_id>:<actor_name>}
        self.ID_TO_ACTOR = self.open_json('../data/tmdb/id_to_actor.json')
        # dict: {<actor_name>:<actor_id>}
        self.ACTOR_TO_ID = self.open_json('../data/tmdb/actor_to_id.json')
        # dict {<tmdb_id>: List[<actor_id1>, <actor_id2>, <actor_id3>]}
        self.ACTORS_BY_MOVIE = cast.load_movie_actors_from_json('../data/tmdb/top_three_actors_by_movie.json')
        self.TMDB_INFO = pd.read_csv('../data/tmdb/combined_tmdb_data.csv')
        self.TMDB_INFO['release_year'] = pd.to_datetime(self.TMDB_INFO['release_date']).dt.year
        self.TMDB_INFO = self.TMDB_INFO[['id', 'release_year']]
        self.TMDB_INFO = self.TMDB_INFO.rename(columns={'id':'tmdb_id'})
        self.roi = ComputeROI()
        # dict: {tmdb_id:roi}
        self.ALL_ROI = self.roi.compute_all_roi()
        # full graph
        self.G = self.load_graph('../graph_encoding/actor_graph.gexf')
        # only actors that have been in more than 3 movies together
        self.subG = self.load_graph('../graph_encoding/actor_sub_graph.gexf')

    def open_json(self, file_path:str) -> dict:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

    def build_graph(self):
        # Initialize a MultiGraph instead of a Graph
        G = nx.MultiGraph()

        # nodes for each actor
        for actor_id in self.ID_TO_ACTOR.keys():
            G.add_node(actor_id, name=self.ID_TO_ACTOR[actor_id])
        # Inverting ID_TO_ACTOR to get ACTOR_TO_ID for lookup
        self.ACTOR_TO_ID = {name: id for id, name in self.ID_TO_ACTOR.items()}

        # Then, when adding edges:
        for tmdb_id_str, actor_names in self.ACTORS_BY_MOVIE.items():
            actor_ids = [self.ACTOR_TO_ID[name] for name in actor_names]
            tmdb_id = int(tmdb_id_str)
            if tmdb_id in self.ALL_ROI:
                roi = self.ALL_ROI[tmdb_id]
                release_year = self.TMDB_INFO[self.TMDB_INFO['tmdb_id'] == tmdb_id]['release_year'].iloc[0]

                for i in range(len(actor_ids)):
                    for j in range(i+1, len(actor_ids)):
                        actor_i = actor_ids[i]
                        actor_j = actor_ids[j]
                        # For a multigraph, add_edge will add multiple edges if called multiple times
                        # between the same pair of nodes
                        G.add_edge(actor_i, actor_j, tmdb_id=tmdb_id, release_year=release_year, roi=roi)

        return G
    
    def write_graph(self, G_in, file_path):
        nx.write_gexf(G_in, file_path)


    def get_pairs_with_more_than_k_edges(self, k: int) -> None:
        edge_counts = {}
        
        for u, v in self.G.edges():
            if (u, v) not in edge_counts and (v, u) not in edge_counts:
                num_edges = len(self.G.get_edge_data(u, v))
                if num_edges > k:
                    edge_counts[(min(u, v), max(u, v))] = num_edges

        for pair, num_edges in edge_counts.items():
            print(f'Nodes {pair[0]} and {pair[1]} have {num_edges} edges between them')

    
    def build_sub_graph(self, k:int):
        qual_edges = []
        for u, v, data in self.G.edges(data=True):
            # In a MultiGraph, count all unique edges between u and v
            num_edges = len(self.G.get_edge_data(u, v))
            if num_edges > k:
                # For each qualifying pair, append all individual edge keys
                for key in range(num_edges):
                    qual_edges.append((u, v, key))
        
        # Create a subgraph based on these qualifying edges
        subgraph = self.G.edge_subgraph(qual_edges)
        return subgraph

    def load_graph(self, graph_path):
        graph = nx.read_gexf(graph_path)
        return graph
    
    def get_actor_id_by_name(self, actor_name:str):
        for id, name in self.ACTOR_IDS.items():
            if name == actor_name:
                return id
        return '-1'
    
    def lookup_actor_pair(self, graph: MultiGraph, actor_a: str, actor_b: str, year: float):
        actor_a = str(actor_a)
        actor_b = str(actor_b)

        actor_a_id = self.ACTOR_TO_ID.get(actor_a, '-1') if not actor_a.isdigit() else actor_a
        actor_b_id = self.ACTOR_TO_ID.get(actor_b, '-1') if not actor_b.isdigit() else actor_b

        actor_a_id = str(actor_a_id)
        actor_b_id = str(actor_b_id)

        edge_data_list = []
        edges = nx.edge_boundary(graph, [actor_a_id], [actor_b_id])
        for u, v in edges:
            for key in graph[u][v]:
                edge_data = graph[u][v][key]
                if edge_data.get('release_year', float('inf')) < year:
                    if edge_data not in edge_data_list:
                        edge_data_list.append(edge_data)

        return edge_data_list


    def print_nodes(self, graph: MultiGraph):
        for node, data in graph.nodes(data=True):
            print(f"ID: {node}, Name: {data.get('name', 'N/A')}")
