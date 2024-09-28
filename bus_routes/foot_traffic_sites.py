import requests

url = "https://besttime.app/api/v1/venues/search"

params = {
    'api_key_private': 'pri_12a0e8c578af422d9279c8cf3cc36970',
    'q': 'busy tourist places, stores, and restaurants in Atlanta Georgia',
    'num': 20,
    'fast': False,
    'format': 'none',
    'busy_min': 80
}

response = requests.request("POST", url, params=params)
print(response.json())