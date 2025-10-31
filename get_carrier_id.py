import os
import requests
from dotenv import load_dotenv

dotenv_path = 'secrets/pondsupportbot2/bequick-token.env'
load_dotenv(dotenv_path)

API_TOKEN = os.getenv("BEQUICK_TOKEN")

url = "https://pondmobile-atom-api.bequickapps.com/carriers"
headers = {
    "X-AUTH-TOKEN": API_TOKEN,
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)
print(response.status_code)
print(response.text)
