# auth.py
import os
import re
import requests
from dotenv import load_dotenv
from pathlib import Path

# === Load BeQuick API token ===
BASE_DIR = Path(__file__).resolve().parent
dotenv_path = BASE_DIR / "secrets" / "pondsupportbot2" / "bequick-token.env"

if not os.path.exists(dotenv_path):
    raise FileNotFoundError(f"[ERROR] File bequick-token.env not found at {dotenv_path}")

load_dotenv(dotenv_path)

API_TOKEN = os.getenv("bequick_token")
if not API_TOKEN:
    raise ValueError("[ERROR] bequick_token not loaded from bequick-token.env")


# === Normalize phone number ===
def normalize_mdn(phone_number: str) -> str:
    """
    Приводит номер телефона к формату, понятному BeQuick API:
    - удаляет все символы, кроме цифр;
    - убирает код страны 1 (для номеров США).
    """
    digits = re.sub(r"\D", "", phone_number)
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    return digits


# === Verify customer and get line_id ===
def get_line_id(mdn: str):
    """
    Проверяет, существует ли MDN (номер телефона) в BeQuick
    и возвращает line_id, если найден.
    Возвращает None, если не найден.
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
    Возвращает True, если номер найден в системе BeQuick (то есть клиент Pond Mobile).
    """
    return get_line_id(mdn) is not None