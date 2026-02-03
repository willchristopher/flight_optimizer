
import requests

CLIENT_ID = 'ZZbrHOMjTDQvN2JxG2ObLkPvfzPYZw32'
CLIENT_SECRET = 'xBwvKAoAZppiAk9w'

def get_amadeus_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    payload = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    headers = { 'Content-Type': 'application/x-www-form-urlencoded' }

    response = requests.post(url, data=payload, headers=headers)
    response.raise_for_status()
    return response.json()["access_token"]

def get_flight_offers(origin, destination, date='2025-05-15', adults=1):
    token = get_amadeus_token()
    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    params = {
        'originLocationCode': origin,
        'destinationLocationCode': destination,
        'departureDate': date,
        'adults': adults,
        'max': 3,
        'currencyCode': 'USD'
    }
    headers = { 'Authorization': f'Bearer {token}' }

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()