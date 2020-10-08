import requests
# the base url for where all requests start
BASE = "http://127.0.0.1:5000"

response = requests.put(f"{BASE}/video/1", {"likes": 10})

print(response.json())