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
    """Generate a random date within the specified month and year."""
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
    """Randomly return a value or None based on the null probability."""
    return value if random.random() > NULL_PROBABILITY else None

def generate_flight_data():
    """Generate flight data and save it to JSON files."""
    os.makedirs('./flights', exist_ok=True)  # Ensure base directory exists

    for i in range(NUM_FILES):
        origin_city = random.choice(cities)
        month = random.randint(1, 12)
        year = random.randint(2021, 2024)
        
        # Ensure unique filename by using a counter `i` in the filename
        file_path = f"./flights/{month:02d}-{year}-{origin_city}-{i+1}.json"

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
            with open(file_path, 'w') as f:
                json.dump(flights, f, indent=2)
        except IOError as e:
            print(f"Error writing to file {file_path}: {e}")

    print(f"Generated {NUM_FILES} JSON files with random flight data.")
    return f"Generated {NUM_FILES} JSON files with random flight data."

# Uncomment the following line to run as a standalone script.
# if __name__ == "__main__":
#     generate_flight_data()
