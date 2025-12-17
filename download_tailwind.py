
import requests

url = "https://cdn.tailwindcss.com"
response = requests.get(url)

with open("assets/js/tailwindcss.js", "w") as f:
    f.write(response.text)
