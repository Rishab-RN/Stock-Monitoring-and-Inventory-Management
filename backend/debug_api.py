import requests
try:
    response = requests.get("http://localhost:8000/api/products?limit=5")
    print(f"Status Code: {response.status_code}")
    print(f"Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
