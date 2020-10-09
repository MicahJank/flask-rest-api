import requests
# the base url for where all requests start
BASE = "http://127.0.0.1:5000"

# response = requests.put(f"{BASE}/video/1", {"likes": 10, "name": "Micah", "views": 100000})
# print(response.json())
# input()
response = requests.get(f"{BASE}/video/6")
print(response.json())
