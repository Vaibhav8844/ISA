
# import gpxpy
# import pandas as pd
# import numpy as np
# from geopy.distance import geodesic
# import folium
# from scipy.spatial import KDTree
# from datetime import datetime, timedelta
# import requests
# import pywhatkit as kit
# from dotenv import load_dotenv
# import os

# load_dotenv()
# razorpay_key_id = os.getenv('RAZORPAY_KEY_ID')
# razorpay_key_secret = os.getenv('RAZORPAY_KEY_SECRET')
# # razorpay_key_id = ""
# # razorpay_key_secret = ""

# # Dictionary to track toll exits and timestamps
# toll_exit_times = {}

# # Function to generate UPI link
# def generate_upi_link(upi_id, name, amount):
#     return f"upi://pay?pa={upi_id}&pn={name}&am={amount}&cu=INR"

# # Function to send WhatsApp message
# def send_whatsapp_message(phone_number, message):
#     now = datetime.now() + timedelta(minutes=1)  # Send 1 minute later
#     hour, minute = now.hour, now.minute
#     kit.sendwhatmsg(phone_number, message, hour, minute)
#     print("WhatsApp message scheduled successfully.")

# # # Function to send payment request
# # def send_payment_request(toll_name, amount):
# #     upi_id = "9075785450@upi"   # Replace with your UPI ID
# #     name ="Toll "+toll_name       # Replace with your name
# #     phone_number = "+919075785450"  # Replace with your WhatsApp number

# #     # Generate UPI Link
# #     upi_link = generate_upi_link(upi_id, name, amount)
# #     message = f"Payment for {toll_name}: ?{amount:.2f}\nUPI Link: {upi_link}"
    
# #     # Send WhatsApp message
# #     send_whatsapp_message(phone_number, message)
# #     print(f"Payment request for {toll_name} created successfully.")


# def send_payment_request(toll_name, amount, customer_phone, customer_name="Customer"):
#     # Razorpay Payment Links API endpoint
#     url = "https://api.razorpay.com/v1/payment_links"
    
    
#     # Payment details
#     data = {
#         "amount": int(amount * 100),  # Amount in paise
#         "currency": "INR",
#         "accept_partial": False,
#         "description": f"Payment for {toll_name}",
#         "customer": {
#             "name": customer_name,
#             "contact": customer_phone
#         },
#         "notify": {
#             "sms": True,  # Enable SMS notification
#             "email": False
#         },
#         "reminder_enable": True
#     }
    
#     # Make the API request to Razorpay
#     response = requests.post(url, json=data, auth=(razorpay_key_id, razorpay_key_secret))
    
#     if response.status_code == 200:
#         payment_data = response.json()
#         print(f"Payment request for {toll_name} created successfully.")
        
#         # Extract the payment link
#         payment_link_id = payment_data['id']
#         payment_link = payment_data['short_url']
#         status = "Pending"
#         timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         print(f"Payment Link: {payment_link}")
        
#         print("SMS sent to customer with the payment link.")


#         # Log the payment details in CSV
#         payment_log = {
#             "Payment Link ID": payment_link_id,
#             "Toll Name": toll_name,
#             "Amount": amount,
#             "Customer Phone": customer_phone,
#             "Payment Link": payment_link,
#             "Status": status,
#             "Timestamp": timestamp
#         }
        
#         # Append to CSV
#         try:
#             df = pd.read_csv('payment_status.csv')
#             df = pd.concat([df, pd.DataFrame([payment_log])], ignore_index=True)
#         except FileNotFoundError:
#             df = pd.DataFrame([payment_log])
        
#         df.to_csv('payment_status.csv', index=False)
        
#         print(f"Payment link recorded in payment_status.csv.")
#     else:
#         print("Failed to create payment request:", response.json())


# def update_payment_status():
#     try:
#         df = pd.read_csv('payment_status.csv')
#     except FileNotFoundError:
#         print("No payment records found.")
#         return
    
#     for index, row in df.iterrows():
#         if row["Status"] == "Pending":
#             payment_link_id = row["Payment Link ID"]
#             url = f"https://api.razorpay.com/v1/payment_links/{payment_link_id}"
#             response = requests.get(url, auth=(razorpay_key_id , razorpay_key_secret))
            
#             if response.status_code == 200:
#                 payment_data = response.json()
#                 status = payment_data['status']
#                 df.at[index, "Status"] = status.capitalize()
#                 print(f"Updated status for {payment_link_id}: {status}")
#             else:
#                 print("Failed to fetch payment status:", response.json())
    
#     # Save updated statuses to the CSV file
#     df.to_csv('payment_status.csv', index=False)
#     print("Payment statuses updated in payment_status.csv.")





# # Function to read a GPX file and extract coordinates
# def read_gpx_file(file_path):
#     with open(file_path, 'r') as gpx_file:
#         gpx = gpxpy.parse(gpx_file)
#         return [(point.latitude, point.longitude, point.elevation) 
#                 for track in gpx.tracks for segment in track.segments for point in segment.points]


# # Function to read toll zones from a CSV file and create a KD-Tree
# def read_toll_zones(csv_path, radius=10000):
#     df = pd.read_csv(csv_path)
#     toll_zones = [{"name": row['Toll Plaza Name'], 
#                    "center": (row['Latitude'], row['Longitude']), 
#                    "radius": radius} 
#                   for _, row in df.iterrows()]
    
#     zone_coords = np.array([(zone["center"][0], zone["center"][1]) for zone in toll_zones])
#     toll_tree = KDTree(zone_coords)
    
#     return toll_zones, toll_tree


# # Function to check if a point is within a toll zone using KD-Tree
# def is_within_toll_zone(lat, lon, toll_zones, toll_tree):
#     indices = toll_tree.query_ball_point([lat, lon], 30 / 111)  # Approximate conversion of km to degrees
#     nearby_toll_zones = [toll_zones[i] for i in indices]
    
#     return next((zone for zone in nearby_toll_zones if geodesic((lat, lon), zone['center']).meters <= zone['radius']), None)


# # Function to check if the movement is in the direction of the toll zone
# def is_in_direction_of_propagation(prev_point, current_point, toll_center):
#     bearing_prev_to_current = calculate_bearing(prev_point, current_point)
#     bearing_current_to_toll = calculate_bearing(current_point, toll_center)
    
#     # Check if the bearing difference is within a certain threshold (e.g., 45 degrees)
#     return abs(bearing_prev_to_current - bearing_current_to_toll) < 20


# # Function to calculate bearing between two points
# def calculate_bearing(point1, point2):
#     lat1, lon1 = np.radians(point1)
#     lat2, lon2 = np.radians(point2)
#     dlon = lon2 - lon1

#     x = np.sin(dlon) * np.cos(lat2)
#     y = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(dlon)
#     bearing = np.degrees(np.arctan2(x, y))
#     return (bearing + 360) % 360  # Normalize to 0-360 degrees


# # Function to calculate the total distance traveled in toll zones
# def calculate_toll_distance(gps_coordinates, toll_zones, toll_tree, toll_rate_per_meter):
#     total_distance = 0.0
#     previous_point = None
#     active_zone = None
#     toll_details = {}  # To store distance and cost per toll zone

#     for lat, lon, _ in gps_coordinates:
#         current_point = (lat, lon)
        
#         # If already inside a toll zone, continue tracking it
#         if active_zone:
#             # Check if still within the active zone
#             if is_within_toll_zone(lat, lon, toll_zones, toll_tree) == active_zone:
#                 if previous_point:
#                     distance = geodesic(previous_point, current_point).meters
#                     total_distance += distance
#                     toll_details[active_zone["name"]]["distance"] += distance
#             else:
#                 # Exiting the active toll zone
#                 print(f"Exiting {active_zone['name']} at {current_point}")
#                 exit_time = datetime.now()
#                 toll_exit_times[active_zone["name"]] = exit_time
#                 active_zone = None
        
#         # If not in any active toll zone, check for a new one
#         if not active_zone:
#             potential_zone = is_within_toll_zone(lat, lon, toll_zones, toll_tree)
            
#             if potential_zone and previous_point:
#                 # Check direction of propagation
#                 if is_in_direction_of_propagation(previous_point, current_point, potential_zone["center"]):
#                     active_zone = potential_zone
#                     print(f"Entering {active_zone['name']} at {current_point}")
                    

#                     # If exiting and re-entering within 30 minutes, reset exit time
#                     if (active_zone["name"] in toll_exit_times and 
#                         datetime.now() - toll_exit_times[active_zone["name"]] < timedelta(minutes=30)):
#                         print(f"Re-entered {active_zone['name']} within 30 minutes. No payment triggered.")
#                         toll_exit_times.pop(active_zone["name"])


#                     # Initialize toll details if encountering for the first time
#                     if active_zone["name"] not in toll_details:
#                         toll_details[active_zone["name"]] = {"distance": 0.0, "cost": 0.0}
        
#         previous_point = current_point

#     # Calculate individual costs for each toll zone
#     for zone_name, details in toll_details.items():
#         distance_km = details["distance"] / 1000
#         cost = distance_km * toll_rate_per_meter
#         toll_details[zone_name]["cost"] = cost

#         if zone_name in toll_exit_times:
#             exit_time = toll_exit_times[zone_name]
#             if datetime.now() - exit_time >= timedelta(microseconds=1):
#                 print(f"No re-entry within 30 minutes. Sending payment request for {zone_name}")
#                 update_payment_status()  # Check for pending payments
#                 # send_payment_request(zone_name, cost)
#                 send_payment_request(toll_name="Toll "+zone_name, amount=cost, customer_phone="919075785450")
#                 toll_exit_times.pop(zone_name)  # Remove after payment

#     return total_distance, toll_details


# # Function to visualize the route and mark toll zones
# def visualize_gpx_route_with_toll_zones(gps_coordinates, toll_zones, toll_tree):
#     route_map = folium.Map(location=gps_coordinates[0][:2], zoom_start=13)
#     route = [(lat, lon) for lat, lon, _ in gps_coordinates]

#     for lat, lon, _ in gps_coordinates:
#         zone = is_within_toll_zone(lat, lon, toll_zones, toll_tree)
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
#     toll_zones, toll_tree = read_toll_zones(csv_file_path)

#     toll_rate_per_meter = 3.2857  # Fixed cost factor per km
#     total_distance, toll_details = calculate_toll_distance(gps_coordinates, toll_zones, toll_tree, toll_rate_per_meter)
    
#     print("\nTotal distance traveled in toll zones: {:.2f} meters".format(total_distance))
#     total_toll_fee = sum(details["cost"] for details in toll_details.values())
#     print(f"Total Toll Fee: ?{total_toll_fee:.2f}\n")

#     print("Detailed Breakdown by Toll Zone:")
#     for zone_name, details in toll_details.items():
#         distance_km = details["distance"] / 1000
#         cost = details["cost"]
#         print(f"{zone_name}: Distance = {distance_km:.2f} km, Cost = ?{cost:.2f}")

#     visualize_gpx_route_with_toll_zones(gps_coordinates, toll_zones, toll_tree)
#     update_payment_status()






import pandas as pd
import numpy as np
from geopy.distance import geodesic
from scipy.spatial import KDTree
import time
import gpsd
import folium
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv
import os


load_dotenv()
razorpay_key_id = os.getenv('RAZORPAY_KEY_ID')
razorpay_key_secret = os.getenv('RAZORPAY_KEY_SECRET')
last_t=""


# Dictionary to track toll exits and timestamps
toll_exit_times = {}



def send_payment_request(toll_name, amount, customer_phone, customer_name="Customer"):
    # Razorpay Payment Links API endpoint
    url = "https://api.razorpay.com/v1/payment_links"
    
    
    # Payment details
    data = {
        "amount": int(amount * 100),  # Amount in paise
        "currency": "INR",
        "accept_partial": False,
        "description": f"Payment for {toll_name}",
        "customer": {
            "name": customer_name,
            "contact": customer_phone
        },
        "notify": {
            "sms": True,  # Enable SMS notification
            "email": False
        },
        "reminder_enable": True
    }
    
    # Make the API request to Razorpay
    response = requests.post(url, json=data, auth=(razorpay_key_id, razorpay_key_secret))
    
    if response.status_code == 200:
        payment_data = response.json()
        print(f"Payment request for {toll_name} created successfully.")
        
        # Extract the payment link
        payment_link_id = payment_data['id']
        payment_link = payment_data['short_url']
        status = "Pending"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Payment Link: {payment_link}")
        
        print("SMS sent to customer with the payment link.")


        # Log the payment details in CSV
        payment_log = {
            "Payment Link ID": payment_link_id,
            "Toll Name": toll_name,
            "Amount": amount,
            "Customer Phone": customer_phone,
            "Payment Link": payment_link,
            "Status": status,
            "Timestamp": timestamp
        }
        
        # Append to CSV
        try:
            df = pd.read_csv('payment_status.csv')
            df = pd.concat([df, pd.DataFrame([payment_log])], ignore_index=True)
        except FileNotFoundError:
            df = pd.DataFrame([payment_log])
        
        df.to_csv('payment_status.csv', index=False)
        
        print(f"Payment link recorded in payment_status.csv.")
    else:
        print("Failed to create payment request:", response.json())


def update_payment_status():
    try:
        df = pd.read_csv('payment_status.csv')
    except FileNotFoundError:
        print("No payment records found.")
        return
    
    for index, row in df.iterrows():
        if row["Status"] == "Pending":
            payment_link_id = row["Payment Link ID"]
            url = f"https://api.razorpay.com/v1/payment_links/{payment_link_id}"
            response = requests.get(url, auth=(razorpay_key_id , razorpay_key_secret))
            
            if response.status_code == 200:
                payment_data = response.json()
                status = payment_data['status']
                df.at[index, "Status"] = status.capitalize()
                print(f"Updated status for {payment_link_id}: {status}")
            else:
                print("Failed to fetch payment status:", response.json())
    
    # Save updated statuses to the CSV file
    df.to_csv('payment_status.csv', index=False)
    print("Payment statuses updated in payment_status.csv.")



# Function to read toll zones from a CSV file and create a KD-Tree
def read_toll_zones(csv_path, radius=75):
    df = pd.read_csv(csv_path)
    toll_zones = [{"name": row['Toll Plaza Name'], 
                   "center": (row['Latitude'], row['Longitude']), 
                   "radius": radius} 
                  for _, row in df.iterrows()]
    
    zone_coords = np.array([(zone["center"][0], zone["center"][1]) for zone in toll_zones])
    toll_tree = KDTree(zone_coords)
    
    return toll_zones, toll_tree


# Function to check if a point is within a toll zone using KD-Tree
def is_within_toll_zone(lat, lon, toll_zones, toll_tree):
    indices = toll_tree.query_ball_point([lat, lon], 30 / 111)  # Approximate conversion of km to degrees
    nearby_toll_zones = [toll_zones[i] for i in indices]
    
    return next((zone for zone in nearby_toll_zones if geodesic((lat, lon), zone['center']).meters <= zone['radius']), None)


def is_in_direction_of_propagation(prev_point, current_point, toll_center):
    bearing_prev_to_current = calculate_bearing(prev_point, current_point)
    bearing_current_to_toll = calculate_bearing(current_point, toll_center)
    
    # Check if the bearing difference is within a certain threshold (e.g., 45 degrees)
    return abs(bearing_prev_to_current - bearing_current_to_toll) < 20


# Function to calculate bearing between two points
def calculate_bearing(point1, point2):
    lat1, lon1 = np.radians(point1)
    lat2, lon2 = np.radians(point2)
    dlon = lon2 - lon1

    x = np.sin(dlon) * np.cos(lat2)
    y = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(dlon)
    bearing = np.degrees(np.arctan2(x, y))
    return (bearing + 360) % 360  # Normalize to 0-360 degrees

def send_payment_if_no_reentry():
    """Check if any toll zone was exited 30 minutes ago without re-entry and trigger payment."""
    current_time = datetime.now()
    for toll_name, exit_time in list(toll_exit_times.items()):
        if current_time - exit_time >= timedelta(minutes=30):
            print(f"No re-entry into {toll_name} for 30 minutes. Sending payment request.")
            update_payment_status()  # Check for pending payments
            # send_payment_request(zone_name, cost)
            send_payment_request(toll_name="Toll "+zone_name, amount=toll_details[zone_name]["cost"], customer_phone="919075785450")
            toll_exit_times.pop(toll_name)  # Remove from tracking after payment


# Function to calculate the total distance traveled in toll zones
def calculate_toll_distance(toll_zones, toll_tree, toll_rate_per_meter):
    total_distance = 0.0
    previous_point = None
    active_zone = False
    toll_details = {}
    last_toll=""

    # Initialize GPSD
    gpsd.connect()
    
    print("Waiting for GPS signal...")

    #while time.time() - start_time < 20:
    while True:
        report = gpsd.get_current()
        
        if report.mode < 2:  # No GPS fix
            print("No GPS fix yet. Waiting...")
            time.sleep(1)
            continue
        
        lat, lon = report.position()  # Get GPS coordinates
        alt = getattr(report, 'alt', 0.0)

        current_point = (lat, lon)
        # print(f"\nProcessing GPS point: Latitude: {lat}, Longitude: {lon}, Altitude: {alt}")
        print(f"Active Toll Zone: {active_zone['name'] if active_zone else None}")
        # Check if currently in an active toll zone
        if active_zone:
            print(f"Currently in toll zone: {active_zone['name']}")
            last_toll=active_zone['name']
            if is_within_toll_zone(lat, lon, toll_zones, toll_tree) == active_zone:
                if previous_point:
                    distance = geodesic(previous_point, current_point).meters
                    total_distance += distance
                    toll_details[active_zone["name"]]["distance"] += distance
                    print(f"Distance in {active_zone['name']}: {distance:.2f} meters")
                    last_t=active_zone['name']
            else:
                print(f"Exiting {active_zone['name']} at {current_point}")
                exit_time = datetime.now()
                last_toll=active_zone['name']
                toll_exit_times[active_zone["name"]] = exit_time
                active_zone = None
        
        # Check if entering a new toll zone
        if not active_zone:
            
            potential_zone = is_within_toll_zone(lat, lon, toll_zones, toll_tree)
            print(f"Potential Zone: {potential_zone['name'] if potential_zone else None}")
            print(f"Previous Point: {previous_point}")
            if potential_zone and previous_point:
                # if is_in_direction_of_propagation(previous_point, current_point, potential_zone["center"]):
                    active_zone = potential_zone
                    print(f"Entering {active_zone['name']} at {current_point}")
                    last_toll=active_zone['name']

                    if (active_zone["name"] in toll_exit_times and 
                        datetime.now() - toll_exit_times[active_zone["name"]] < timedelta(minutes=1)):
                        print(f"Re-entered {active_zone['name']} within 30 minutes. No payment triggered.")
                        toll_exit_times.pop(active_zone["name"])
                    # elif(active_zone["name"] in toll_exit_times and 
                    #     datetime.now() - toll_exit_times[active_zone["name"]] >= timedelta(minutes=1)):
                    #     print(f"No re-entry within 30 minutes. Sending payment request for {zone_name}")
                    #     update_payment_status()  # Check for pending payments
                    #     # send_payment_request(zone_name, cost)
                    #     send_payment_request(toll_name="Toll "+zone_name, amount=toll_details[zone_name]["cost"], customer_phone="919075785450")
                    #     toll_exit_times.pop(zone_name)
                    elif(active_zone["name"] in toll_exit_times and 
                        datetime.now() - toll_exit_times[active_zone["name"]] >= timedelta(minutes=1)):
                        print(f"No re-entry within 30 minutes. Sending payment request for {last_toll}")
                        update_payment_status()
                        send_payment_request(toll_name="Toll "+active_zone["name"], amount=toll_details[active_zone["name"]]["cost"], customer_phone="919075785450")
                        toll_exit_times.pop(active_zone["name"])


                    if active_zone["name"] not in toll_details:
                        toll_details[active_zone["name"]] = {"distance": 0.0, "cost": 0.0}
                
                # if active_zone["name"] not in toll_details:
                #     toll_details[active_zone["name"]] = {"distance": 0.0, "cost": 0.0}
            elif(not potential_zone and previous_point and last_toll!=""):
                        active_zone = potential_zone
                # print(active_zone["name"])
                        if(datetime.now()-toll_exit_times[last_toll]>=timedelta(seconds=10) and (last_toll in toll_details)):
                            print(f"No re-entry within 30 minutes. Sending payment request for {last_toll}")
                            update_payment_status()
                            send_payment_request(toll_name="Toll "+last_toll, amount=toll_details[last_toll]["distance"]*toll_rate_per_meter, customer_phone="919075785450")
                            send_payment_request(toll_name="Toll "+last_toll, amount=toll_details[last_toll]["distance"]*toll_rate_per_meter, customer_phone="919691924419")
                            del toll_details[last_toll]
                            # toll_exit_times.pop(last_toll)
            else:
                print(f"Not in a toll zone - Latitude: {lat}, Longitude: {lon}, Altitude: {alt}")
                
        previous_point = current_point

        # send_payment_if_no_reentry()    
        
        
        
        time.sleep(5)

    # Calculate toll cost
    for zone_name, details in toll_details.items():
        details["cost"] = (details["distance"] / 1000) * toll_rate_per_meter
        print(f"Total in {zone_name}: {details['distance'] / 1000:.2f} km, Cost: ?{details['cost']:.2f}")

    return total_distance, toll_details


# Function to visualize the route and mark toll zones
def visualize_route_with_toll_zones(gps_coordinates, toll_zones, toll_tree):
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
    csv_file_path = "coordinates_india.csv"  # Path to CSV containing toll zones
    
    # Read toll zones and create KD-Tree for fast lookup
    toll_zones, toll_tree = read_toll_zones(csv_file_path)

    toll_rate_per_meter = 3.2857  # Cost per meter
    start_time = time.time()  # Get the start time
    toll_details = None
    total_distance = 0
    

    total_distance, toll_details = calculate_toll_distance(toll_zones, toll_tree, toll_rate_per_meter)
    send_payment_request(toll_name="Toll ", amount=total_distance*toll_rate_per_meter, customer_phone="919075785450")
    print("Request Sent")
    print("\nTotal distance traveled in toll zones: {:.2f} meters".format(total_distance))
    total_toll_fee = total_distance*toll_rate_per_meter
    print(f"Total Toll Fee: {total_toll_fee:.2f}\n")

    print("Detailed Breakdown by Toll Zone:")
    for zone_name, details in toll_details.items():
        print(f"{zone_name}: Distance = {details['distance'] / 1000:.2f} km, Cost = ?{details['cost']:.2f}")
          
