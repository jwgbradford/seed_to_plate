import requests, json

resource = 'val/wxfcs/all/json/31004'
api_key = open('/home/w-s/Documents/ApiKey/weather_api.txt', 'r').readlines()[0].rstrip()
url = f'http://datapoint.metoffice.gov.uk/public/data/{resource}?res=daily&key={api_key}'
data = json.loads(requests.get(url).text)
print(data)