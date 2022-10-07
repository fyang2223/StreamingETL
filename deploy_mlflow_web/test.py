import requests

features = {
    "t1":2, 
    "t2":3,
    "hum":50,
    "weather_code":2
}

url = 'http://localhost:9696/predict'

response = requests.post(url, json=features)

print(response.json())





