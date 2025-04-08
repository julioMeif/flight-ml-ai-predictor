from flight_search import search_flights
from flight_search_internal import search_internal_flights
from datetime import datetime, timedelta
import pandas as pd
import time

queries = [
    {'origin': 'NYC', 'destination': 'LON', 'trip_type': 'ONE_WAY', 'airlines': ['UA', 'BA'] , 'sources': ['amadeus']},
    {'origin': 'LAX', 'destination': 'LHR', 'trip_type': 'ONE_WAY', 'airlines': ['UA', 'BA'], 'sources': ['amadeus']},
    {'origin': 'NYC', 'destination': 'TYO', 'trip_type': 'ONE_WAY', 'airlines': ['CX', 'TG'], 'sources': ['amadeus']},
    {'origin': 'MIA', 'destination': 'MAD', 'trip_type': 'ONE_WAY', 'sources': ['amadeus']},
]

def fetch_batch_flights(start_date, days_ahead):
    all_flights = []
    for day_offset in range(days_ahead):
        departure_date = (start_date + timedelta(days=day_offset)).strftime("%Y-%m-%d")

        for query in queries:
            return_date = (datetime.strptime(departure_date, "%Y-%m-%d") + timedelta(days=query.get('return_days_after', 0))).strftime("%Y-%m-%d") if query['trip_type'] == "ROUND_TRIP" else None
            sources = query.get('sources', ['amadeus'])

            for source in sources:
                print(f"[{source.upper()}] Fetching global search {query['trip_type']} from {query['origin']} to {query['destination']} on {departure_date}...")

                try:
                    if source == 'amadeus':
                        responses = search_internal_flights(
                            query['origin'],
                            query['destination'],
                            departure_date,
                            return_date=return_date,
                            trip_type=query['trip_type']
                        )
                    else:
                        responses = search_flights(
                            query['origin'],
                            query['destination'],
                            departure_date,
                            trip_type=query['trip_type'],
                            return_date=return_date,
                            source=source
                        )

                    for resp in responses:
                        flights = parse_response(resp, query, departure_date, airline=None)
                        all_flights.extend(flights)
                        time.sleep(0.2)

                    for airline in query.get('airlines', []):
                        print(f"[{source.upper()}] Fetching airline-specific ({airline}) from {query['origin']} to {query['destination']} on {departure_date}...")
                        if source == 'amadeus':
                            responses_airline = search_internal_flights(
                                query['origin'],
                                query['destination'],
                                departure_date,
                                return_date=return_date,
                                trip_type=query['trip_type'],
                                airline=airline
                            )
                        else:
                            responses_airline = search_flights(
                                query['origin'],
                                query['destination'],
                                departure_date,
                                trip_type=query['trip_type'],
                                return_date=return_date,
                                airline=airline,
                                source=source
                            )

                        for resp in responses_airline:
                            flights_airline = parse_response(resp, query, departure_date, airline=airline)
                            all_flights.extend(flights_airline)
                            time.sleep(0.2)

                except Exception as e:
                    print(f"Error fetching {departure_date}, {query} from {source}: {e}")

    df = pd.DataFrame(all_flights)
    df.to_csv("../data/flights_data_extended.csv", index=False)
    print("Extended data saved to ../data/flights_data_extended.csv")


def parse_response(response, query, departure_date, airline=None):
    flights = []
    source = response['source']
    offers = response['data'].get('best_flights', []) + response['data'].get('other_flights', []) if source == 'google_flights' else response['data']

    for offer in offers:
        if source == 'amadeus':
            segments = offer['itineraries'][0]['segments']
            segment_airlines = '-'.join([seg['carrierCode'] for seg in segments])
            flight_numbers = '-'.join([seg['number'] for seg in segments])
            stops = len(segments) - 1
            duration = offer['itineraries'][0]['duration']
            departure_time = departure_date
            price = float(offer['price']['total'])
            currency = offer['price']['currency']

        elif source == 'google_flights':
            segments = offer['flights']
            segment_airlines = segments[0]['airline']
            flight_numbers = '-'.join([seg['flight_number'].replace(' ', '') for seg in segments])
            stops = len(segments) - 1
            duration = f"PT{offer['total_duration']}M"
            departure_time = segments[0]['departure_airport']['time'][:10] if 'time' in segments[0]['departure_airport'] else departure_date
            price = float(offer['price'])
            currency = response['data'].get('search_parameters', {}).get('currency', 'USD')

        flights.append({
            'departure_date': departure_time,
            'origin': query['origin'],
            'destination': query['destination'],
            'trip_type': query['trip_type'],
            'requested_airline': airline if airline else 'ALL',
            'actual_airlines': segment_airlines,
            'flight_numbers': flight_numbers,
            'stops': stops,
            'duration': duration,
            'price': price,
            'currency': currency,
            'source': source
        })

    return flights


if __name__ == "__main__":
    start = datetime(2025, 7, 1)
    days_to_fetch = 60
    fetch_batch_flights(start, days_to_fetch)
