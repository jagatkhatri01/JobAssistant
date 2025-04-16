import requests

url = "https://jsearch.p.rapidapi.com/estimated-salary"

querystring = {"job_title":"nodejs developer","location":"new york","location_type":"ANY","years_of_experience":"ALL"}

headers = {
	"x-rapidapi-key": "b832c6dbd2mshd2a807ea29d5cb2p13a81cjsnc7497c3b8d0a",
	"x-rapidapi-host": "jsearch.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())