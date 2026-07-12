import requests

url = "https://www.daggegevens.knmi.nl/klimatologie/daggegevens"

response = requests.get(url)

print("Status:", response.status_code)
print(response.text[:500])
