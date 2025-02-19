import time

def simulate_gps_movement(gps_coordinates):
    for lat, lon, elev in gps_coordinates:
        print(f"Simulated GPS Location -> Latitude: {lat}, Longitude: {lon}, Elevation: {elev}")
        time.sleep(1)  # Delay to simulate movement

# Simulate GPS movement
simulate_gps_movement(gps_coordinates)
