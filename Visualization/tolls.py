import folium
import pandas as pd

# Read the CSV file containing toll data (name, Latitude, Longitude)
toll_data = pd.read_csv("E:\HAM\ham-project\ISA\coordinates_india.csv")

# Create a base map centered around an approximate central point
# You can adjust the initial location as per the data's geographical center
map_center = [toll_data["Latitude"].mean(), toll_data["Longitude"].mean()]
m = folium.Map(location=map_center, zoom_start=10)

# Function to create a popup with toll details
def create_popup(toll):
    popup_html = f"""
    <h4>{toll['Toll Plaza Name']}</h4>
    <p><b>Latitude:</b> {toll['Latitude']}</p>
    <p><b>Longitude:</b> {toll['Longitude']}</p>
    """
    return folium.Popup(popup_html, max_width=300)

# Iterate through each row in the CSV to create markers
for index, row in toll_data.iterrows():
    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=create_popup(row),
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# Save the map to an HTML file
m.save("Visualization/toll_map.html")

print("Map with toll markers saved as 'toll_map.html'.")
