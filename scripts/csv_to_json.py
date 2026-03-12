# Import statements
import os
import csv
import json

def csv_to_json_func(csv_file):
    """
    Convert a CSV file to JSON format.

    Args:
        csv_file (str): Path to the CSV file.

    Returns:
        str: Path to the generated JSON file.
    """
    json_file = os.path.splitext(csv_file)[0] + ".json"
    data = []
    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)

    with open(json_file, "w") as file:
        json.dump(data, file, indent=4)
    print("CSV successfully converted to JSON")
    return json_file