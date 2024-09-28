import csv
import requests

def get_distance(lat1, lon1, lat2, lon2, api_key):
    api_url = 'https://api.distancematrix.ai/maps/api/distancematrix/json'
    params = {
        'origins': f'{lat1},{lon1}',
        'destinations': f'{lat2},{lon2}',
        'key': '1sI7IyZD6I2wf0fVzQX4kbmyFA2gvP8m9XJsgJR65UtkQttw9qegisPoMLLrvrT8'
    }

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['status'] == "OK":
            distance = data['rows'][0]['elements'][0]['distance']['text']
            duration = data['rows'][0]['elements'][0]['duration']['text']
            return distance , duration
        else:
            raise ValueError(f"Error from API: {data['status']}")
    else:
        raise ValueError(f"Failed to fetch data from Distance Matrix API. Status code: {response.status_code}")

def read_csv_and_calculate_distances(csv_file, api_key):
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        # Get the top 2 entries
        locations = [next(reader) for _ in range(2)]

        # Extract the relevant details
        venue1 = locations[0]
        venue2 = locations[1]

        name1, address1, lat1, lon1 = venue1['venue_name'], venue1['venue_address'], venue1['latitude'], venue1['longitude']
        name2, address2, lat2, lon2 = venue2['venue_name'], venue2['venue_address'], venue2['latitude'], venue2['longitude']

        # Print venue details
        print(f"Calculating distance between:\n1. {name1} ({address1})\n2. {name2} ({address2})")
        
        # Calculate distance
        distance, duration = get_distance(lat1, lon1, lat2, lon2, api_key)

        # Print the results
        print(f"Distance: {distance}, Duration: {duration}")

if __name__ == "__main__":
    API_KEY = 'YOUR_ACCESS_TOKEN'  # Replace with your actual API key
    CSV_FILE = 'static/foot_traffic_sites.csv'  # Adjust the path if necessary

    read_csv_and_calculate_distances(CSV_FILE, API_KEY)
