import os
import json
import numpy as np
from collections import defaultdict
import time

def process_flight_data(directory='./flights'):
    total_records = 0
    dirty_records = 0
    flight_durations = []
    passenger_count = defaultdict(lambda: {'arrived': 0, 'departed': 0})
    start_time = time.time()

    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, 'r') as f:
                    flights = json.load(f)
                    total_records += len(flights)

                    for flight in flights:
                        if any(value is None for value in flight.values()):
                            dirty_records += 1
                            continue

                        flight_duration = flight['flight_duration_secs']
                        flight_durations.append(flight_duration)

                        origin = flight['origin_city']
                        destination = flight['destination_city']
                        passenger_count[origin]['departed'] += flight.get('passengers_on_board', 0)
                        passenger_count[destination]['arrived'] += flight.get('passengers_on_board', 0)

            except Exception as e:
                print(f"Error processing file {filename}: {e}")

    avg_duration = np.mean(flight_durations) if flight_durations else 0
    p95_duration = np.percentile(flight_durations, 95) if flight_durations else 0

    destination_counts = {city: data['arrived'] for city, data in passenger_count.items()}
    top_25_destinations = sorted(destination_counts.items(), key=lambda x: x[1], reverse=True)[:25]

    max_passengers_arrived_city = max(passenger_count.items(), key=lambda x: x[1]['arrived'], default=(None, {'arrived': 0}))
    max_passengers_departed_city = max(passenger_count.items(), key=lambda x: x[1]['departed'], default=(None, {'departed': 0}))

    total_run_duration = time.time() - start_time

    # Output results
    print(f"Total records processed: {total_records}")
    print(f"Total dirty records: {dirty_records}")
    print(f"Total run duration: {total_run_duration:.2f} seconds")
    print(f"Average flight duration: {avg_duration:.2f} seconds")
    print(f"P95 flight duration: {p95_duration:.2f} seconds")
    print("Top 25 destination cities with passenger counts:")
    for city, count in top_25_destinations:
        print(f"{city}: {count} passengers")
    print(f"City with max passengers arrived: {max_passengers_arrived_city[0]} ({max_passengers_arrived_city[1]['arrived']} passengers)")
    print(f"City with max passengers departed: {max_passengers_departed_city[0]} ({max_passengers_departed_city[1]['departed']} passengers)")


    return {
        "total_records": total_records,
        "dirty_records": dirty_records,
        "run_duration_seconds": total_run_duration,
        "avg_flight_duration": avg_duration,
        "p95_flight_duration": p95_duration,
        "top_25_destinations": top_25_destinations,
        "max_arrivals": max_passengers_arrived_city,
        "max_departures": max_passengers_departed_city
    }

# Just uncomment below line if you want to run standalone file.
# process_flight_data() 
