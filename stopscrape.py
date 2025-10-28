import requests
import csv

# Output CSV file
output_file = "MPK_stops.csv"

# CSV header
header = ["id", "name", "lat", "long", "street"]

with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(header)


    for stop_id in range(1, 2601):
        url = f"https://services.mpk.amistad.pl/mpk/schedule/stop/{stop_id}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                stop = data.get("stop")
                if stop and "positions" in stop and stop["positions"]:
                    row = [
                        stop.get("id"),
                        stop.get("name"),
                        stop["positions"][0].get("lat"),
                        stop["positions"][0].get("lng"),
                        stop.get("street")
                    ]
                    writer.writerow(row)
        except Exception as e:
            print(f"Error with stop ID {stop_id}: {e}")
