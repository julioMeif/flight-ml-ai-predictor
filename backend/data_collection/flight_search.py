import requests
import os
from credentials import AMADEUS_CLIENT_ID, AMADEUS_CLIENT_SECRET, SERPAPI_KEY
from dotenv import load_dotenv

load_dotenv()

API_ENDPOINT = os.getenv("AMADEUS_API_ENDPOINT")

def get_amadeus_access_token():
    url = f"{API_ENDPOINT}/v1/security/oauth2/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": AMADEUS_CLIENT_ID,
        "client_secret": AMADEUS_CLIENT_SECRET
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

def search_amadeus_flights(origin, destination, departure_date, trip_type="ONE_WAY", return_date=None, airline=None):
    try:
        token = get_amadeus_access_token()
        url = f"{API_ENDPOINT}/v2/shopping/flight-offers"
        headers = {"Authorization": f"Bearer {token}"}

        params = {
            'originLocationCode': origin,
            'destinationLocationCode': destination,
            'departureDate': departure_date,
            'adults': 1,
            'currencyCode': 'USD'
        }

        if trip_type == "ROUND_TRIP" and return_date:
            params['returnDate'] = return_date

        if airline:
            params['includedAirlineCodes'] = airline

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return {'source': 'amadeus', 'data': response.json()}

    except Exception as e:
        print(f"[Amadeus] Error fetching data: {e}")
        return {'source': 'amadeus', 'error': str(e)}

def search_google_flights(origin, destination, departure_date, trip_type="ONE_WAY", return_date=None, airline=None):
    try:
        url = "https://serpapi.com/search.json"
        params = {
            "engine": "google_flights",
            "departure_id": origin,
            "arrival_id": destination,
            "hl": "en",
            "gl":"us",
            "outbound_date": departure_date,
            "currency":"USD",
            "api_key": SERPAPI_KEY
        }
        
        if trip_type == "ONE_WAY":
            params["type"] = 2

        if trip_type == "ROUND_TRIP" and return_date:
            params["return_date"] = return_date

        if airline:
            params["include_airlines"] = airline

        #print(params)

        response = requests.get(url, params=params, verify=False)
        response.raise_for_status()
        return {'source': 'google_flights', 'data': response.json()}

    except Exception as e:
        print(f"[Google Flights] Error fetching data: {e}")
        return {'source': 'google_flights', 'error': str(e)}

def search_flights(origin, destination, departure_date, trip_type="ONE_WAY", return_date=None, airline=None, source=['amadeus','google_flights']):
    results = []
    if 'amadeus' in source:
        results.append(search_amadeus_flights(origin, destination, departure_date, trip_type, return_date, airline))
    if 'google_flights' in source:
        results.append(search_google_flights(origin, destination, departure_date, trip_type, return_date, airline))
    return results

if __name__ == "__main__":
    flights = search_flights("MIA", "CDG", "2025-07-25", trip_type="ONE_WAY", airline="AF")
    for result in flights:
        print(f"\nSource: {result['source']}")
        if 'data' in result:
            print(result['data'])
        else:
            print(f"Error: {result['error']}")
