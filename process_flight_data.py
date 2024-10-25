import os
import json
import numpy as np
from datetime import datetime
from collections import defaultdict
import time
from glob import glob
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_file(file_path, passenger_count, flight_durations):
    """Process a single JSON file and update counts and durations."""
    local_total_records = 0
    local_dirty_records = 0
    try:
        with open(file_path, 'r') as f:
            flights = json.load(f)
            local_total_records += len(flights)

            for flight in flights:
                if any(value is None for value in flight.values()):
                    local_dirty_records += 1
                    continue

                flight_duration = flight['flight_duration_secs']
                flight_durations.append(flight_duration)

                origin = flight['origin_city']
                destination = flight['destination_city']
                passenger_count[origin]['departed'] += flight.get('passengers_on_board', 0)
                passenger_count[destination]['arrived'] += flight.get('passengers_on_board', 0)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
    return local_total_records, local_dirty_records

def process_flight_data(directory='./flights'):
    """Process all JSON files in the directory concurrently and return structured results."""
    total_records = 0
    dirty_records = 0
    flight_durations = []
    passenger_count = defaultdict(lambda: {'arrived': 0, 'departed': 0})
    start_time = time.time()

    file_paths = glob(os.path.join(directory, '*.json'))

    # Use ThreadPoolExecutor for concurrent file processing
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_file, file_path, passenger_count, flight_durations) for file_path in file_paths]
        
        for future in as_completed(futures):
            records, dirties = future.result()
            total_records += records
            dirty_records += dirties

    # Calculate statistics
    avg_duration = np.mean(flight_durations) if flight_durations else 0
    p95_duration = np.percentile(flight_durations, 95) if flight_durations else 0
    total_run_duration = time.time() - start_time

    # Determine top 25 destination cities and max arrivals/departures
    destination_counts = {city: data['arrived'] for city, data in passenger_count.items()}
    top_25_destinations = sorted(destination_counts.items(), key=lambda x: x[1], reverse=True)[:25]
    max_arrivals = max(passenger_count.items(), key=lambda x: x[1]['arrived'], default=(None, {'arrived': 0}))
    max_departures = max(passenger_count.items(), key=lambda x: x[1]['departed'], default=(None, {'departed': 0}))

    # Return structured results
    return {
        "total_records": total_records,
        "dirty_records": dirty_records,
        "run_duration_seconds": total_run_duration,
        "avg_flight_duration": avg_duration,
        "p95_flight_duration": p95_duration,
        "top_25_destinations": top_25_destinations,
        "max_arrivals": max_arrivals[0],  # city name with max arrivals
        "max_departures": max_departures[0]  # city name with max departures
    }

# Just uncomment below line if you want to run standalone file.
# if __name__ == "__main__":
#     results = process_flight_data()
#     print(json.dumps(results, indent=2))
