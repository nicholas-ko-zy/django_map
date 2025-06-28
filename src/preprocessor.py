import osmnx as ox
import numpy as np
import pandas as pd
import networkx as nx
import pickle

class Preprocessor:
    def __init__(self):
        # Load graph of road network in Singapore
        graph_path = "data/SG_nodes.pkl"

        with open(graph_path, 'rb') as f: 
            # notice the r instead of w
            G = pickle.load(f)

        G = ox.routing.add_edge_speeds(G)
        G = ox.routing.add_edge_travel_times(G)
        self.G = G

    def calculate_route(self, x1, y1, x2, y2):
        """_summary_

        Args:
            x1 (_type_): Lon value of source location
            y1 (_type_): Lat value of source location
            x2 (_type_): Lon value of sink location
            y2 (_type_): Lat value of sink location
        """
        orig = ox.distance.nearest_nodes(self.G, X=x1, Y=y1)
        dest = ox.distance.nearest_nodes(self.G, X=x2, Y=y2)
        n_cpus = 4
        print(f'Solving shortest path with {n_cpus} CPUs...')
        route = ox.routing.shortest_path(self.G, orig, dest, weight="travel_time", cpus=n_cpus)
        return route

    def get_route_distance(self, x1, y1, x2, y2):
        route = self.calculate_route(x1, y1, x2, y2)
        edge_lengths = ox.routing.route_to_gdf(self.G, route)["length"]
        distance = round(sum(edge_lengths))
        return distance
    
    