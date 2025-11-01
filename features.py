import os
import requests
from dotenv import load_dotenv
from pathlib import Path
from config import API_URL, API_TOKEN

print("[DEBUG] Loaded features.py from:", __file__)

# === Load BeQuick token ===
dotenv_path = 'secrets/pondsupportbot2/bequick.env'
load_dotenv(dotenv_path)
API_URL = "https://pondmobile-atom-api.bequickapps.com"

API_TOKEN = os.getenv("BEQUICK_TOKEN")
if not API_TOKEN:
    raise ValueError("Token not found in bequick.env")


# === Convert KB → MB/GB string ===
def kb_to_readable(kb_value: float) -> str:

    mb = kb_value / 1024
    if mb >= 1024:
        gb = mb / 1024
        return f"{gb:.3f} GB"
    return f"{mb:.2f} MB"

# === Fetch data usage ===
def check_usage(line_id: int | str):

    url = f"{API_URL}/lines/{line_id}/query_service_details"
    headers = {"X-AUTH-TOKEN": API_TOKEN, "Content-Type": "application/json"}

    print(f"[BeQuick Usage] Checking usage for line_id={line_id} at: {url}")

    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"[BeQuick Usage] Status: {response.status_code}")
        print(f"[BeQuick Usage] Response sample: {(response.text or '')[:400]}")

        if response.status_code != 200:
            return f"📊 Unable to fetch usage (status {response.status_code})"

        data = response.json() or {}
        usage_summary = data.get("usage_summary", {})
        data_usage = usage_summary.get("international_data", {})

        # Extract values (in kilobytes)
        total_kb = float(data_usage.get("total", 0))
        remaining_kb = float(data_usage.get("remaining", 0))
        used_kb = float(data_usage.get("used_by_this_line", data_usage.get("used", 0)))

        print(f"[DEBUG] Raw KB: used={used_kb}, total={total_kb}, remaining={remaining_kb}")

        # Convert to readable units
        used_str = kb_to_readable(used_kb)
        total_str = kb_to_readable(total_kb)
        remaining_str = kb_to_readable(remaining_kb)

        print(f"[DEBUG] Converted: used={used_str}, total={total_str}, remaining={remaining_str}")

        return f"📊 Used: {used_str}"

    except requests.exceptions.RequestException as e:
        print(f"[BeQuick Usage] Connection error: {e}")
        return "📊 Error fetching usage data"



import os
import requests

dotenv_path = 'secrets/pondsupportbot2/bequick.env'
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
