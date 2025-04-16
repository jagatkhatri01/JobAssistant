import requests
from django.conf import settings
from urllib.parse import quote

def fetch_jobs(query="python", location="", page=1):
    """Simplified version matching your working curl request"""
    url = f"https://api.adzuna.com/v1/api/jobs/us/search/{page}"
    
    config = settings.ADZUNA_CONFIG
    
    params = {
        'app_id': config['APP_ID'],
        'app_key': config['API_KEY'],
        'what': quote(query.lower())
    }
    # Only add location if specified
    if location:
        params['where'] = quote(location.lower())
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get('results', [])
    except Exception as e:
        print(f"API Error: {str(e)}")
        if hasattr(e, 'response'):
            print("Error details:", e.response.text)
        return []