from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from jnius import autoclass
import numpy as np
from geopy.distance import geodesic
from scipy.spatial import KDTree
import pandas as pd

# Android GPS Access
PythonActivity = autoclass('org.kivy.android.PythonActivity')
LocationManager = autoclass('android.location.LocationManager')
Context = autoclass('android.content.Context')

class GPSApp(App):
    def build(self):
        self.label = Label(text="Fetching GPS...")
        Clock.schedule_interval(self.update_gps, 5)  # Update every 5 sec
        return self.label

    def update_gps(self, dt):
        location_service = PythonActivity.mActivity.getSystemService(Context.LOCATION_SERVICE)
        gps_provider = LocationManager.GPS_PROVIDER
        location = location_service.getLastKnownLocation(gps_provider)

        if location:
            lat, lon = location.getLatitude(), location.getLongitude()
            self.label.text = f"Lat: {lat}, Lon: {lon}"

            # Check if within toll zone
            toll_zone = is_within_toll_zone(lat, lon, toll_zones, toll_tree)
            if toll_zone:
                self.label.text += f"\nToll Zone: {toll_zone['name']}"

# Load Toll Zones from CSV
def read_toll_zones(csv_path, radius=15000):
    df = pd.read_csv(csv_path)
    toll_zones = [{"name": row['name'], "center": (row['latitude'], row['longitude']), "radius": radius} 
                  for _, row in df.iterrows()]
    zone_coords = np.array([(zone["center"][0], zone["center"][1]) for zone in toll_zones])
    toll_tree = KDTree(zone_coords)
    return toll_zones, toll_tree

# Fast Toll Zone Check
def is_within_toll_zone(lat, lon, toll_zones, toll_tree):
    indices = toll_tree.query_ball_point([lat, lon], 30 / 111)
    nearby_toll_zones = [toll_zones[i] for i in indices]
    return next((zone for zone in nearby_toll_zones if geodesic((lat, lon), zone['center']).meters <= zone['radius']), None)

# Load Toll Zones
csv_file_path = "/mnt/data/coordinates_india.csv"
toll_zones, toll_tree = read_toll_zones(csv_file_path)

if __name__ == "__main__":
    GPSApp().run()
