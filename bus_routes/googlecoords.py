import requests

def get_lat_long(address):
    # Hardcoded API key
    api_key = 'AIzaSyB0KYyn_tG8Ob0ng1ecIioUcCETcM3c5Kg'  # Replace with your actual API key
    
    # URL for the Geocoding API
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    
    # Send a GET request to the Geocoding API
    response = requests.get(url)
    
    # Parse the JSON response
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            # Extract latitude and longitude
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            print("Error: ", data['status'])
            return None
    else:
        print("HTTP Error: ", response.status_code)
        return None

# Example usage
if __name__ == '__main__':
    address = '1600 Amphitheatre Parkway, Mountain View, CA'
    lat, lng = get_lat_long(address)

    if lat and lng:
        print(f"Latitude: {lat}, Longitude: {lng}")
    else:
        print("Could not retrieve coordinates.")
