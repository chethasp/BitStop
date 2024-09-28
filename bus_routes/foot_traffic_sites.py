import requests
import json
import time
import csv

thanish_api_key = 'pri_12a0e8c578af422d9279c8cf3cc36970'
thanish_api_key2 = 'pri_b22c7fdcc1c64ffb81bc9365bbba2640'
thanish_api_key3 = 'pri_632cd4c106bb49ecaf9cd44f616c7cc4'
thanish_api_key4 = 'pri_93f8fa30e75c4464a21f573c02608c29'

def get_foot_traffic_sites(min_business, city, place_amt, api_key):

    initial_search_url = "https://besttime.app/api/v1/venues/search"

    params = {
        'api_key_private': api_key,
        'q': 'popular places in {location}'.format(location = city),
        'num': place_amt,
        'fast': False,
        'format': 'none',
        'busy_min': min_business
    }

    initial_search_response = requests.request("POST", initial_search_url, params=params)

    initial_search_json = json.loads(json.dumps(initial_search_response.json()))

    venues_result_url = "https://besttime.app/api/v1/venues/progress"

    params2 = {
        'job_id': initial_search_json['job_id'],
        'collection_id': initial_search_json['collection_id'],
        'format': 'raw'
    }

    print("waiting for venues...\n")

    time.sleep(5)

    venues_result_response = requests.request("GET", venues_result_url, params=params2)
    
    venues_response_json = venues_result_response.json();

    time_elapsed = 0

    while venues_response_json['job_finished'] == False:
        venues_result_response = requests.request("GET", venues_result_url, params=params2)
    
        venues_response_json = venues_result_response.json();   

        print("time elapsed: {time}, job finished? {job_status}, waiting...\n".format(time=time_elapsed, job_status=venues_response_json['job_finished']))
        #print(venues_response_json)

        time_elapsed += 10

        time.sleep(10)     


    result_dict = json.loads(json.dumps(venues_response_json))

    results_arr = result_dict['venues']

    print("\n\ngetting top {count} places with footraffic over {pct}% in {location}: \n".format(count=place_amt, pct=min_business, location=city))

    result = [['venue_name', 'venue_address', 'latitude', 'longitude', 'foot_traffic']]

    counter = 1

    for venue in results_arr:
        print(venue['venue_name'] + ": " + venue['venue_address'] + '\n')
        result.append([venue['venue_name'], venue['venue_address'], venue['venue_lat'], venue['venue_lon'], counter])
        counter += 1


    with open('static/foot_traffic_sites.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(result)

    with open('static/previous_collections.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([params['q'], params2['collection_id']])

    return result


get_foot_traffic_sites(80, "Atlanta, Georgia", 100, thanish_api_key4)

