from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
    View
)
# from rest_framework.views import APIView
# from rest_framework.response import Response
from django.contrib.gis.geos import Point
import pydeck as pdk
from django.conf import settings
import os
import re
import folium
from .utils import make_markers_and_add_to_map
import xyzservices.providers as xyz
import folium.plugins as plugins
from django.http import JsonResponse, HttpResponseBadRequest
import requests
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import json
import numpy as np
import csv

class HomeMapView(TemplateView):
    template_name = 'map/index.html'
  
class CsvUploadView(View):
    def post(self, request, *args, **kwargs):
        # Check if a file is uploaded
        csv_file = request.FILES.get('file')
        if not csv_file:
            return HttpResponseBadRequest("No file uploaded")

        # Read and decode CSV file
        try:
            data = csv_file.read().decode('utf-8')
            io_string = io.StringIO(data)
            reader = csv.DictReader(io_string)
        except Exception as e:
            return HttpResponseBadRequest(f"Error reading CSV file: {e}")

        locations = []
        # Expected CSV columns: name, lat, lon
        for row in reader:
            try:
                name = row['name']
                lat = float(row['lat'])
                lon = float(row['lon'])
                locations.append({"name": name, "lat": lat, "lon": lon})
            except (KeyError, ValueError):
                # Skip rows with missing or invalid data
                continue

        return JsonResponse({"locations": locations})

class SolveRouteView(View):
    """
    Class-based view for handling vehicle routing requests
    """
    
    def post(self, request, *args, **kwargs):
        try:
            # 1. Get coordinates from frontend
            data = json.loads(request.body)
            locations = data['coordinates']
            print(locations)
            # 2. Process routing
            distance_matrix = self.get_distance_matrix(locations)
            print(f'Distance matrix: {distance_matrix}')
            print(f'Locations: {locations}')
            vehicle_routes = self.solve_vrp(distance_matrix)
            print(f'Vehicle routes: {vehicle_routes}')
            
            vehicle_paths = self.get_vehicle_paths(locations, vehicle_routes)
            # 3. Prepare response with routes included
            return self.build_response(vehicle_paths, vehicle_routes)
            
        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON"},
                status=400
            )
        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": str(e)},
                status=500
            )

    def get_distance_matrix(self, locations):
        """Get OSRM distance matrix"""
        coords_str = ";".join([f"{lon},{lat}" for lat, lon in locations])
        url = f"http://router.project-osrm.org/table/v1/driving/{coords_str}"
        resp = requests.get(url, params={"annotations": "distance"})
        resp.raise_for_status()
        # Change pairwise distance matrix entries to all type int
        pairwise_dist_matrix = np.array(resp.json()['distances'])
        pairwise_dist_matrix_int = pairwise_dist_matrix.astype(int)
        return pairwise_dist_matrix_int

    def solve_vrp(self, distance_matrix, num_vehicles=4, depot=0, max_distance=1000):
        """Solve Vehicle Routing Problem with distance constraints
        
        Args:
            distance_matrix: 2D array of distances between locations
            num_vehicles: Number of vehicles in the fleet
            depot: Index of the depot/start location
            max_distance: Maximum distance each vehicle can travel
        
        Returns:
            List of routes (each route is a list of node indices)
        """
        # Create routing index manager
        manager = pywrapcp.RoutingIndexManager(
            len(distance_matrix), 
            num_vehicles, 
            depot
        )
        
        # Create routing model
        routing = pywrapcp.RoutingModel(manager)

        # Define distance callback
        def distance_callback(from_index, to_index):
            """Returns the distance between the two nodes."""
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return distance_matrix[from_node][to_node]

        # Register distance callback
        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        
        # Set arc cost evaluator
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        
        # Add Distance constraint
        dimension_name = "Distance"
        routing.AddDimension(
            transit_callback_index,
            0,  # no slack
            200000,  # vehicle maximum travel distance
            True,  # start to zero
            dimension_name
        )
        distance_dimension = routing.GetDimensionOrDie(dimension_name)
        distance_dimension.SetGlobalSpanCostCoefficient(100)

        # Setting first solution heuristic
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )

        search_parameters.time_limit.seconds = 10  # Limit solve time
        search_parameters.log_search = False  # Enable logging?

        # Solve the problem
        solution = routing.SolveWithParameters(search_parameters)
        
        # Extract routes from solution
        routes = []
        if solution:
            for route_nbr in range(routing.vehicles()):
                index = routing.Start(route_nbr)
                route = [manager.IndexToNode(index)]
                while not routing.IsEnd(index):
                    index = solution.Value(routing.NextVar(index))
                    route.append(manager.IndexToNode(index))
                routes.append(route)
        else:
            print("No solution found!")
        return routes

    def get_vehicle_paths(self, locations, vehicle_routes):
        """Get detailed route geometries for each vehicle"""
        vehicle_paths = []
        
        for route in vehicle_routes:
            if len(route) < 2:
                # Skip empty routes
                continue
                
            waypoints = [locations[i] for i in route]
            coords_str = ';'.join(f"{lon},{lat}" for lat, lon in waypoints)
            
            resp = requests.get(
                f"http://router.project-osrm.org/route/v1/driving/{coords_str}",
                params={"overview": "full", "geometries": "geojson", "continue_straight": "false"}
            )
        
            data = resp.json()
            # TODO: Deal with case where there is no route between points
            vehicle_paths.append({
                "geometry": data['routes'][0]['geometry'],
                "distance": data['routes'][0]['distance'],
                "duration": data['routes'][0]['duration'],
                "waypoints": waypoints
            })
        return vehicle_paths
    
    def build_response(self, vehicle_paths, vehicle_routes):
        """Structure the API response with route indices included"""
        return JsonResponse({
            "status": "success",
            "vehicles": [
                {
                    "path": path['geometry']['coordinates'],
                    "summary": {
                        "distance_km": round(path['distance'] / 1000, 2),
                        "duration_min": round(path['duration'] / 60, 1),
                        # Optionally include waypoints here if needed:
                        # "waypoints": path['waypoints'],
                    },
                    "route_indices": vehicle_routes[i]  # Add the visiting order indices here
                }
                for i, path in enumerate(vehicle_paths)
            ]
        })


