import os
import urllib.parse
from dotenv import load_dotenv


# === Load text prompt ===
def load_prompt(name: str) -> str:
    path = f"resources/{name}.txt"
    if not os.path.exists(path):
        raise FileNotFoundError(f"[ERROR] File not found: {path}")
    with open(path, "r", encoding="utf8") as file:
        return file.read()


# === Load token from .env file ===
def load_token(name: str) -> str:
    dotenv_path = f"secrets/pondsupportbot2/{name}.env"
    if not os.path.exists(dotenv_path):
        raise FileNotFoundError(f"[ERROR] Env file not found: {dotenv_path}")

    load_dotenv(dotenv_path)
    token = os.getenv(f"{name.upper()}_TOKEN")
    if not token:
        raise ValueError(f"[ERROR] {name} token not found in {dotenv_path}")
    return token


# === Telegram support deep-link with prefilled message ===
def refresh_line(mdn: str) -> str:

    base_url = "https://t.me/pondsupport"
    message = f"Dear customer support, this is my number {mdn}, please refresh my line"
    encoded = urllib.parse.quote(message)
    return f"{base_url}?text={encoded}"
