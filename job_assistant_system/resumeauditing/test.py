import http.client

conn = http.client.HTTPSConnection("indeed12.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "ea0236f372msh9fd669837ac11ddp1ed68ejsn814609f78ba7",
    'x-rapidapi-host': "indeed12.p.rapidapi.com"
}

conn.request("GET", "/jobs/search?query=manager&location=pokhara", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))