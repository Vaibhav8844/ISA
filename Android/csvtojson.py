import pandas as pd
import json

def convert_csv_to_json(csv_file, json_file):
    df = pd.read_csv(csv_file)
    df.to_json(json_file, orient="records", indent=4)

csv_path = "E:\HAM\ham-project\ISA\coordinates_india.csv"  # Your CSV file
json_path = "toll_zones.json"  # Output JSON file

convert_csv_to_json(csv_path, json_path)
print(f"CSV converted to JSON and saved as {json_path}")
