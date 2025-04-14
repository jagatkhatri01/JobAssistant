from django.shortcuts import render

# Create your views here.
import http.client
import json
from django.shortcuts import render
from django.conf import settings

def job_listings(request):
    # API connection setup
    conn = http.client.HTTPSConnection("indeed12.p.rapidapi.com")
    
    # Get query parameters from request
    query = request.GET.get('query', 'manager')
    location = request.GET.get('location', 'us')
    
    headers = {
        'x-rapidapi-key': "ea0236f372msh9fd669837ac11ddp1ed68ejsn814609f78ba7",
        'x-rapidapi-host': "indeed12.p.rapidapi.com"
    }
    
    try:
        # Make API request
        conn.request("GET", f"/jobs/search?query={query}&location={location}", headers=headers)
        res = conn.getresponse()
        data = res.read()
        json_response = json.loads(data.decode("utf-8"))
        
        # Prepare context for template
        context = {
            'jobs': json_response.get('hits', []),
            'query': query,
            'location': location,
            'total_jobs': len(json_response.get('hits', [])),
            'search_performed': True
        }
        
    except Exception as e:
        context = {
            'error': str(e),
            'search_performed': False
        }
    
    return render(request, 'jobs/listings.html', context)