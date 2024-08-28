import requests 

def get_coordinates(address):
    api_key = 'YOUR_API_KEY'
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}'
    response = requests.get(url)
    results = response.json().get('results')
    if results:
        location = results[0].get('geometry', {}).get('location', {})
        return location.get('lat'), location.get('lng')
    return None, None
