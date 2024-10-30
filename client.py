import requests

url = "http://127.0.0.1:8000/projects/"  # Replace with your API endpoint

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    print("Data:", data)
else:
    print("Failed to retrieve data:", response.text, "\n\n")
