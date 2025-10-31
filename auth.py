# auth.py
import os
import re
import requests
from dotenv import load_dotenv
from pathlib import Path

print("[DEBUG] Loaded auth.py from:", __file__)

# === Load token ===
BASE_DIR = Path(__file__).resolve().parent
dotenv_path = BASE_DIR / "secrets" / "pondsupportbot2" / "bequick-token.env"
load_dotenv(dotenv_path)

API_TOKEN = os.getenv("bequick_token")
if not API_TOKEN:
    raise ValueError("[ERROR] bequick_token not loaded from bequick-token.env")
else:
    print(f"[DEBUG] Loaded bequick_token: {API_TOKEN[:10]}...")

# === Normalize phone number ===
def normalize_mdn(phone_number: str) -> str:
    """Removes +, spaces, and country code (1) if present."""
    digits = re.sub(r"\D", "", phone_number)
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    return digits

# === Verify customer and get line_id ===
def get_line_id(mdn: str):
    """
    Checks if MDN exists in BeQuick and returns its line_id.
    Returns None if not found.
    """
    clean_mdn = normalize_mdn(mdn)
    url = f"https://pondmobile-atom-api.bequickapps.com/lines?by_quick_find[]={clean_mdn}"
    headers = {"X-AUTH-TOKEN": API_TOKEN, "Content-Type": "application/json"}

    print(f"[DEBUG] Checking MDN: {clean_mdn}")
    print(f"[DEBUG] URL: {url}")

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        print(f"[BeQuick] Status: {resp.status_code}")

        if resp.status_code != 200:
            print(f"[BeQuick] Error response: {resp.text}")
            return None

        data = resp.json() or {}
        lines = data.get("lines", [])
        if not lines:
            print("[DEBUG] No lines found for this MDN.")
            return None

        line_id = lines[0].get("id")
        print(f"[DEBUG] Found line_id: {line_id}")
        return line_id

    except requests.exceptions.RequestException as e:
        print(f"[BeQuick] Connection error: {e}")
        return None

def is_client(mdn: str) -> bool:
    """Returns True if the MDN exists in BeQuick."""
    return get_line_id(mdn) is not None
