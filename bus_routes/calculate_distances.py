import csv
import requests
import re

def get_duration(lat1, lon1, lat2, lon2):
    api_url = 'https://api.distancematrix.ai/maps/api/distancematrix/json'
    api_key = '1sI7IyZD6I2wf0fVzQX4kbmyFA2gvP8m9XJsgJR65UtkQttw9qegisPoMLLrvrT8'
    params = {
        'origins': f'{lat1},{lon1}',
        'destinations': f'{lat2},{lon2}',
        'key': api_key
    }

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['status'] == "OK":
            duration_text = data['rows'][0]['elements'][0]['duration']['text']
            
            # Parse the duration to return a number in minutes
            duration_minutes = 0
            if "hour" in duration_text:
                hours = int(re.search(r'(\d+)\s*hour', duration_text).group(1))
                duration_minutes += hours * 60
            if "min" in duration_text:
                minutes = int(re.search(r'(\d+)\s*min', duration_text).group(1))
                duration_minutes += minutes
            
            return duration_minutes
        else:
            raise ValueError(f"Error from API: {data['status']}")
    else:
        raise ValueError(f"Failed to fetch data from Distance Matrix API. Status code: {response.status_code}")

def read_csv_and_calculate_duration(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        # Get the top 2 entries
        locations = [next(reader) for _ in range(2)]

        # Extract the relevant details
        venue1 = locations[0]
        venue2 = locations[1]

        name1, address1, lat1, lon1 = venue1['venue_name'], venue1['venue_address'], float(venue1['latitude']), float(venue1['longitude'])
        name2, address2, lat2, lon2 = venue2['venue_name'], venue2['venue_address'], float(venue2['latitude']), float(venue2['longitude'])

        # Print venue details
        print(f"Calculating travel duration between:\n1. {name1} ({address1})\n2. {name2} ({address2})")
        
        # Calculate duration
        duration = get_duration(lat1, lon1, lat2, lon2)

        # Print the result
        print(f"Duration: {duration} minutes")

if __name__ == "__main__":
    CSV_FILE = 'static/foot_traffic_sites.csv'  # Adjust the path if necessary

    read_csv_and_calculate_duration(CSV_FILE)
