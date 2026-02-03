
import requests
from amadeus_api import get_flight_offers

API_KEY = '3b670dd3c435781988c3b35ece490ce9'  

def fetch_flights_by_airport(departure_iata):
    url = 'http://api.aviationstack.com/v1/flights'
    params = {
        'access_key': API_KEY,
        'dep_iata': departure_iata,
        'limit': 10
    }

    response = requests.get(url, params=params)
    data = response.json()

    routes = []
    if 'data' in data:
        for flight in data['data']:
            try:
                dep = flight['departure']['iata']
                arr = flight['arrival']['iata']
                airline = flight['airline']['name']
                flight_number = flight['flight']['iata']
                if dep and arr:
                    routes.append((dep, arr, airline, flight_number))
            except (TypeError, KeyError):
                continue
    return routes

def import_real_routes_to_graph(flight_graph, departure_iata):
    flights = fetch_flights_by_airport(departure_iata)
    added = 0

    for dep, arr, airline, flight_num in flights:
        try:
            offers = get_flight_offers(dep, arr)
            real_price = float(offers['data'][0]['price']['total'])
        except Exception as e:
            print(f"Failed price for {dep} → {arr}: {e}")
            continue

        if dep not in flight_graph:
            flight_graph[dep] = []
        if arr not in flight_graph:
            flight_graph[arr] = []
        flight_graph[dep].append((arr, real_price))
        added += 1

    print(f"Imported {added} real flights with prices.")