import http.client

conn = http.client.HTTPSConnection("freelancer-api.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "7dfd568184msh4edaab70036391cp11a7afjsn751be9d2b354",
    'x-rapidapi-host': "freelancer-api.p.rapidapi.com"
}

conn.request("GET", "/find-freelancers/%7Bpage_number%7D", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))