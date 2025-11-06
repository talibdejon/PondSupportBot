# auth.py
import re
import requests
import utils

API_TOKEN = utils.load_token('BEQUICK')
API_URL = "https://pondmobile-atom-api.bequickapps.com"


# === Normalize phone number ===
def normalize_mdn(phone_number: str) -> str:
    digits = re.sub(r"\D", "", phone_number)
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    return digits


# === Verify customer and get line_id ===
def get_line_id(mdn: str):
    clean_mdn = normalize_mdn(mdn)
    url = f"{API_URL}/lines?by_quick_find[]={clean_mdn}"
    headers = {
        "X-AUTH-TOKEN": API_TOKEN,
        "Content-Type": "application/json"
    }

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200:
            print(f"[BeQuick] Error {resp.status_code}: {resp.text}")
            return None

        data = resp.json() or {}
        lines = data.get("lines", [])
        if not lines:
            return None

        return lines[0].get("id")

    except requests.exceptions.RequestException as e:
        print(f"[BeQuick] Connection error: {e}")
        return None


# === Check if user is a Pond Mobile client ===
def is_client(mdn: str) -> bool:
    return get_line_id(mdn) is not None
