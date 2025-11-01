# auth.py
import os
import re
import requests
from dotenv import load_dotenv
from pathlib import Path

from features import API_TOKEN
from utils import load_token

API_TOKEN = load_token('BEQUICK')


# === Normalize phone number ===
def normalize_mdn(phone_number: str) -> str:
    """
    Converts the phone number into a format acceptable for BeQuick API:
    - removes all non-digit characters;
    - removes the country code '1' (for US numbers).
    """
    digits = re.sub(r"\D", "", phone_number)
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    return digits


# === Verify customer and get line_id ===
def get_line_id(mdn: str):
    """
    Checks if the given MDN (phone number) exists in BeQuick
    and returns the line_id if found.
    Returns None if not found.
    """
    clean_mdn = normalize_mdn(mdn)
    url = f"https://pondmobile-atom-api.bequickapps.com/lines?by_quick_find[]={clean_mdn}"
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
    """
    Returns True if the phone number is found in the BeQuick system (i.e., a Pond Mobile client).
    """
    return get_line_id(mdn) is not None