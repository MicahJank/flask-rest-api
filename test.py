import requests
# the base url for where all requests start
BASE = "http://127.0.0.1:5000"

data = [{"likes": 78, "name": "GraphQL for Beginners", "views": 100000}, 
        {"likes": 1100, "name": "Why I am better than you(as a millionare)", "views": 10},
        {"likes": 1, "name": "Top 10 Dev Mistakes", "views": 0},
        {"likes": 90, "name": "Self help 101", "views": 1234},
        {"likes": 130, "name": "Double rainbow", "views": 1294834327},]

# sends out 5 request to make a video
for i,video in enumerate(data):
    response = requests.post(f"{BASE}/video", video)
    print(response.json())  

input()
response = requests.get(f"{BASE}/video/40234")
print(response.json())
input()
response = requests.delete(f"{BASE}/video/1")
print(response.json())
