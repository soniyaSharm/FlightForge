# Flight Data Forge & Processor

A Flask-based application for generating and processing random flight data JSON files. This project includes two main components:
1. **Data Generation**: Creates randomized JSON files with simulated flight data.
2. **Data Processing**: Reads and processes generated JSON files to calculate statistics on flight durations and passenger counts.


## Prerequisites

- **Python 3.8+**
- **pip** for package management

## Setup

1. **Clone the repository**:
   ```bash
   `git clone https://github.com/soniyaSharm/FlightForge.git`
   cd FlightForge

## Create a virtual environment
    python3 -m venv venv

# On Windows activate ENV
    venv\Scripts\activate

# Install the required packages
    pip install -r requirements.txt

# You can use this project in two ways:
1. Run as a Flask Application
    python app.py
2. Run Standalone Scripts


If you prefer not to use the Flask API, you can run each script directly from the command line.
# generate flight data
    python flight_data_forge.py
# process the generated flight data
    python process_flight_data.py

# Use Postman collection
Just import the collection `from tools/postman` to postman and hit the api.
