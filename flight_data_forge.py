import os
import json
import random
from datetime import datetime, timedelta
import calendar

NUM_FILES = 5000  # Number of JSON files
CITY_COUNT = random.randint(100, 200)  # Total unique cities
cities = [f"City_{i}" for i in range(CITY_COUNT)]
NULL_PROBABILITY = random.uniform(0.005, 0.001)  # 0.5% to 0.1%

def random_date(year, month):
    try:
        days_in_month = calendar.monthrange(year, month)[1]
        start_date = datetime(year, month, 1)
        end_date = datetime(year, month, days_in_month)
        random_seconds = random.randint(0, int((end_date - start_date).total_seconds()))
        return start_date + timedelta(seconds=random_seconds)
    except Exception as e:
        print(f"Error generating random date: {e}")
        return None

def maybe_null(value):
    return value if random.random() > NULL_PROBABILITY else None

def generate_flight_data():
    for _ in range(NUM_FILES):
        origin_city = random.choice(cities)
        month = random.randint(1, 12)
        year = random.randint(2021, 2024)
        
        folder_path = f"./flights/{month:02d}-{year}-{origin_city}-flights.json"
        os.makedirs(os.path.dirname(folder_path), exist_ok=True)

        flights = []
        for _ in range(random.randint(50, 100)):
            flight = {
                "date": maybe_null(random_date(year, month).isoformat()),
                "origin_city": maybe_null(origin_city),
                "destination_city": maybe_null(random.choice(cities)),
                "flight_duration_secs": maybe_null(random.randint(3600, 18000)),
                "passengers_on_board": maybe_null(random.randint(1, 300))
            }
            flights.append(flight)

        try:
            with open(folder_path, 'w') as f:
                json.dump(flights, f, indent=2)
        except IOError as e:
            print(f"Error writing to file {folder_path}: {e}")
    print(f"Generated {NUM_FILES} JSON files with random flight data.")
    return f"Generated {NUM_FILES} JSON files with random flight data."

# Just uncomment below line if you want to run standalone file.
# generate_flight_data() 