# import gpxpy
# from geopy.distance import geodesic
# import folium
# import pandas as pd


# # Function to read a GPX file and extract coordinates
# def read_gpx_file(file_path):
#     with open(file_path, 'r') as gpx_file:
#         gpx = gpxpy.parse(gpx_file)
#         coordinates = []

#         # Extract all track points
#         for track in gpx.tracks:
#             for segment in track.segments:
#                 for point in segment.points:
#                     coordinates.append((point.latitude, point.longitude, point.elevation))
#         return coordinates


# # Function to check if a point is within a toll zone
# def is_within_toll_zone(lat, lon, toll_zone):
#     distance = geodesic((lat, lon), toll_zone['center']).meters
#     return distance <= toll_zone['radius']


# # Function to calculate the total distance traveled in a toll zone
# def calculate_toll_distance(gps_coordinates, toll_zone):
#     inside_zone = False
#     total_distance = 0.0
#     previous_point = None

#     for lat, lon, _ in gps_coordinates:
#         current_point = (lat, lon)

#         # Check if the current point is inside the toll zone
#         if is_within_toll_zone(lat, lon, toll_zone):
#             if not inside_zone:
#                 print(f"Entering {toll_zone['name']} at {current_point}")
#             inside_zone = True

#             # Calculate distance if there's a valid previous point
#             if previous_point:
#                 segment_distance = geodesic(previous_point, current_point).meters
#                 total_distance += segment_distance
#         else:
#             if inside_zone:
#                 print(f"Exiting {toll_zone['name']} at {current_point}")
#             inside_zone = False

#         # Update the previous point
#         previous_point = current_point

#     return total_distance


# # Function to visualize the route and mark toll zones
# def visualize_gpx_route_with_toll_zones(gps_coordinates, toll_zones):
#     # Create a map centered on the first GPS point
#     map_center = gps_coordinates[0][:2]
#     route_map = folium.Map(location=map_center, zoom_start=13)

#     # Add markers and lines
#     route = []
#     for lat, lon, _ in gps_coordinates:
#         route.append((lat, lon))
#         in_any_zone = False

#         for zone in toll_zones:
#             if is_within_toll_zone(lat, lon, zone):
#                 folium.CircleMarker(location=(lat, lon), radius=5, color="green", popup=f"Inside {zone['name']}").add_to(route_map)
#                 in_any_zone = True
#                 break

#         if not in_any_zone:
#             folium.CircleMarker(location=(lat, lon), radius=5, color="blue").add_to(route_map)

#     # Draw the route line
#     folium.PolyLine(route, color="red", weight=2.5).add_to(route_map)

#     # Save the map
#     route_map.save("route_map_with_toll_zones.html")
#     print("Route map with toll zones saved as 'route_map_with_toll_zones.html'")


# # Main Code
# if __name__ == "__main__":
#     # Path to your GPX file
#     gpx_file_path = "GPS Route.gpx"  # Replace with the actual path to your GPX file
#     gps_coordinates = read_gpx_file(gpx_file_path)

#     # Define toll zones
#     # toll_zones = [
#     #     {"name": "Toll Zone 1", "center": (17.841703, 79.359844), "radius": 15000},
#     #     {"name": "Toll Zone 2", "center": (17.499716, 78.889544), "radius": 15000}  
#     # ]
#     df = pd.read_csv("coordinates_india.csv")
#     toll_zones=[{"name": row['Toll Plaza Name'], "center": (row['Latitude'], row['Longitude']), "radius": 15000} 
#              for _, row in df.iterrows()]


#     # Calculate the distance traveled in each toll zone
#     for toll_zone in toll_zones:
#         distance_in_zone = calculate_toll_distance(gps_coordinates, toll_zone)
#         print(f"Total distance traveled in {toll_zone['name']}: {distance_in_zone:.2f} meters")

#         # Billing calculation
#         toll_rate_per_meter = 3.2857  # Example rate: 0.01 currency units per meter
#         toll_fee = distance_in_zone * toll_rate_per_meter/1000
#         print(f"Toll Fee for {toll_zone['name']}:₹{toll_fee:.2f}")

#     # Visualize the route with toll zones
#     visualize_gpx_route_with_toll_zones(gps_coordinates, toll_zones)










# import gpxpy
# import pandas as pd
# from geopy.distance import geodesic
# import folium


# # Function to read a GPX file and extract coordinates
# def read_gpx_file(file_path):
#     with open(file_path, 'r') as gpx_file:
#         gpx = gpxpy.parse(gpx_file)
#         return [(point.latitude, point.longitude, point.elevation) 
#                 for track in gpx.tracks for segment in track.segments for point in segment.points]


# # Function to read toll zones from a CSV file
# def read_toll_zones(csv_path, radius=15000):
#     df = pd.read_csv(csv_path)
#     return [{"name": row['Toll Plaza Name'], "center": (row['Latitude'], row['Longitude']), "radius": radius} 
#             for _, row in df.iterrows()]


# # Function to check if a point is within a toll zone
# def is_within_toll_zone(lat, lon, toll_zones):
#     return next((zone for zone in toll_zones if geodesic((lat, lon), zone['center']).meters <= zone['radius']), None)


# # Function to calculate the total distance traveled in toll zones
# def calculate_toll_distance(gps_coordinates, toll_zones):
#     total_distance = 0.0
#     previous_point = None
#     inside_zone = None

#     for lat, lon, _ in gps_coordinates:
#         current_point = (lat, lon)
#         current_zone = is_within_toll_zone(lat, lon, toll_zones)

#         if current_zone:
#             if inside_zone != current_zone:
#                 print(f"Entering {current_zone['name']} at {current_point}")
#             if previous_point:
#                 total_distance += geodesic(previous_point, current_point).meters
#         elif inside_zone:
#             print(f"Exiting {inside_zone['name']} at {current_point}")
        
#         inside_zone = current_zone
#         previous_point = current_point

#     return total_distance


# # Function to visualize the route and mark toll zones
# def visualize_gpx_route_with_toll_zones(gps_coordinates, toll_zones):
#     route_map = folium.Map(location=gps_coordinates[0][:2], zoom_start=13)
#     route = [(lat, lon) for lat, lon, _ in gps_coordinates]

#     for lat, lon, _ in gps_coordinates:
#         zone = is_within_toll_zone(lat, lon, toll_zones)
#         color = "green" if zone else "blue"
#         popup = f"Inside {zone['name']}" if zone else None
#         folium.CircleMarker(location=(lat, lon), radius=5, color=color, popup=popup).add_to(route_map)
    
#     folium.PolyLine(route, color="red", weight=2.5).add_to(route_map)
#     route_map.save("route_map_with_toll_zones.html")
#     print("Route map with toll zones saved as 'route_map_with_toll_zones.html'")


# # Main Code
# if __name__ == "__main__":
#     gpx_file_path = "GPS Route.gpx"
#     csv_file_path = "coordinates_india.csv"
#     gps_coordinates = read_gpx_file(gpx_file_path)
#     toll_zones = read_toll_zones(csv_file_path)

#     total_distance = calculate_toll_distance(gps_coordinates, toll_zones)
#     print(f"Total distance traveled in toll zones: {total_distance:.2f} meters")

#     toll_rate_per_meter = 3.2857  # Example rate
#     toll_fee = total_distance * toll_rate_per_meter / 1000
#     print(f"Total Toll Fee: ₹{toll_fee:.2f}")

#     visualize_gpx_route_with_toll_zones(gps_coordinates, toll_zones)






# import gpxpy
# import pandas as pd
# from geopy.distance import geodesic
# import folium


# # Function to read a GPX file and extract coordinates
# def read_gpx_file(file_path):
#     with open(file_path, 'r') as gpx_file:
#         gpx = gpxpy.parse(gpx_file)
#         return [(point.latitude, point.longitude, point.elevation) 
#                 for track in gpx.tracks for segment in track.segments for point in segment.points]


# # Function to read toll zones from a CSV file
# def read_toll_zones(csv_path, radius=15000):
#     df = pd.read_csv(csv_path)
#     return [{"name": row['Toll Plaza Name'], "center": (row['Latitude'], row['Longitude']), "radius": radius} 
#             for _, row in df.iterrows()]


# # Function to check if a point is within a toll zone (only within 30 km range)
# def is_within_toll_zone(lat, lon, toll_zones):
#     nearby_toll_zones = [zone for zone in toll_zones if geodesic((lat, lon), zone['center']).meters <= 30000]
#     return next((zone for zone in nearby_toll_zones if geodesic((lat, lon), zone['center']).meters <= zone['radius']), None)


# # Function to calculate the total distance traveled in toll zones
# def calculate_toll_distance(gps_coordinates, toll_zones):
#     total_distance = 0.0
#     previous_point = None
#     inside_zone = None

#     for lat, lon, _ in gps_coordinates:
#         current_point = (lat, lon)
#         current_zone = is_within_toll_zone(lat, lon, toll_zones)

#         if current_zone:
#             if inside_zone != current_zone:
#                 print(f"Entering {current_zone['name']} at {current_point}")
#             if previous_point:
#                 total_distance += geodesic(previous_point, current_point).meters
#         elif inside_zone:
#             print(f"Exiting {inside_zone['name']} at {current_point}")
        
#         inside_zone = current_zone
#         previous_point = current_point

#     return total_distance


# # Function to visualize the route and mark toll zones
# def visualize_gpx_route_with_toll_zones(gps_coordinates, toll_zones):
#     route_map = folium.Map(location=gps_coordinates[0][:2], zoom_start=13)
#     route = [(lat, lon) for lat, lon, _ in gps_coordinates]

#     for lat, lon, _ in gps_coordinates:
#         zone = is_within_toll_zone(lat, lon, toll_zones)
#         color = "green" if zone else "blue"
#         popup = f"Inside {zone['name']}" if zone else None
#         folium.CircleMarker(location=(lat, lon), radius=5, color=color, popup=popup).add_to(route_map)
    
#     folium.PolyLine(route, color="red", weight=2.5).add_to(route_map)
#     route_map.save("route_map_with_toll_zones.html")
#     print("Route map with toll zones saved as 'route_map_with_toll_zones.html'")


# # Main Code
# if __name__ == "__main__":
#     gpx_file_path = "GPS Route.gpx"
#     csv_file_path = "coordinates_india.csv"
#     gps_coordinates = read_gpx_file(gpx_file_path)
#     toll_zones = read_toll_zones(csv_file_path)

#     total_distance = calculate_toll_distance(gps_coordinates, toll_zones)
#     print(f"Total distance traveled in toll zones: {total_distance:.2f} meters")

#     toll_rate_per_meter = 3.2857  # Example rate
#     toll_fee = total_distance * toll_rate_per_meter / 1000
#     print(f"Total Toll Fee: ₹{toll_fee:.2f}")

#     # visualize_gpx_route_with_toll_zones(gps_coordinates, toll_zones)








import gpxpy
import pandas as pd
import numpy as np
from geopy.distance import geodesic
import folium
from scipy.spatial import KDTree


# Function to read a GPX file and extract coordinates
def read_gpx_file(file_path):
    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        return [(point.latitude, point.longitude, point.elevation) 
                for track in gpx.tracks for segment in track.segments for point in segment.points]


# Function to read toll zones from a CSV file and create a KD-Tree
def read_toll_zones(csv_path, radius=15000):
    df = pd.read_csv(csv_path)
    toll_zones = [{"name": row['Toll Plaza Name'], "center": (row['Latitude'], row['Longitude']), "radius": radius} 
                  for _, row in df.iterrows()]
    
    zone_coords = np.array([(zone["center"][0], zone["center"][1]) for zone in toll_zones])
    toll_tree = KDTree(zone_coords)
    
    return toll_zones, toll_tree


# Function to check if a point is within a toll zone using KD-Tree
def is_within_toll_zone(lat, lon, toll_zones, toll_tree):
    indices = toll_tree.query_ball_point([lat, lon], 30 / 111)  # Approximate conversion of km to degrees
    nearby_toll_zones = [toll_zones[i] for i in indices]
    
    return next((zone for zone in nearby_toll_zones if geodesic((lat, lon), zone['center']).meters <= zone['radius']), None)


# Function to calculate the total distance traveled in toll zones
def calculate_toll_distance(gps_coordinates, toll_zones, toll_tree):
    total_distance = 0.0
    previous_point = None
    inside_zone = None

    for lat, lon, _ in gps_coordinates:
        current_point = (lat, lon)
        current_zone = is_within_toll_zone(lat, lon, toll_zones, toll_tree)

        if current_zone:
            if inside_zone != current_zone:
                print(f"Entering {current_zone['name']} at {current_point}")
            if previous_point:
                total_distance += geodesic(previous_point, current_point).meters
        elif inside_zone:
            print(f"Exiting {inside_zone['name']} at {current_point}")
        
        inside_zone = current_zone
        previous_point = current_point

    return total_distance


# Function to visualize the route and mark toll zones
def visualize_gpx_route_with_toll_zones(gps_coordinates, toll_zones, toll_tree):
    route_map = folium.Map(location=gps_coordinates[0][:2], zoom_start=13)
    route = [(lat, lon) for lat, lon, _ in gps_coordinates]

    for lat, lon, _ in gps_coordinates:
        zone = is_within_toll_zone(lat, lon, toll_zones, toll_tree)
        color = "green" if zone else "blue"
        popup = f"Inside {zone['name']}" if zone else None
        folium.CircleMarker(location=(lat, lon), radius=5, color=color, popup=popup).add_to(route_map)
    
    folium.PolyLine(route, color="red", weight=2.5).add_to(route_map)
    route_map.save("route_map_with_toll_zones.html")
    print("Route map with toll zones saved as 'route_map_with_toll_zones.html'")


# Main Code
if __name__ == "__main__":
    gpx_file_path = "GPS Route.gpx"
    csv_file_path = "coordinates_india.csv"
    gps_coordinates = read_gpx_file(gpx_file_path)
    toll_zones, toll_tree = read_toll_zones(csv_file_path)

    total_distance = calculate_toll_distance(gps_coordinates, toll_zones, toll_tree)
    print(f"Total distance traveled in toll zones: {total_distance:.2f} meters")

    toll_rate_per_meter = 3.2857  # Example rate
    toll_fee = total_distance * toll_rate_per_meter / 1000
    print(f"Total Toll Fee: ₹{toll_fee:.2f}")

    visualize_gpx_route_with_toll_zones(gps_coordinates, toll_zones, toll_tree)
    