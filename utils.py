import os
import subprocess
import json
import pathlib
import dotenv
import urllib.parse

def load_prompt(name):
    with open(f"resources/{name}.txt", "r", encoding="utf8") as file:
        return file.read()

def load_token(name):
    dotenv_path = 'secrets/pondsupportbot2/'+name+'.env'
    dotenv.load_dotenv(dotenv_path)
    token = os.getenv(f"{name.upper()}_TOKEN")
    if not token:
        raise ValueError(f"[ERROR] {name} token not found in {dotenv_path}")
    return token

def refresh_line(mdn: str) -> str:

    base_url = "https://t.me/pondsupport"
    message = f"Dear customer support, this is my number {mdn}, please refresh my line"
    encoded = urllib.parse.quote(message)
    return f"{base_url}?text={encoded}"
    TOKEN = os.getenv(name.upper()+'_TOKEN')
    if not TOKEN:
        raise ValueError(name+' token not found')
    return TOKEN

STAT_FILE = pathlib.Path("stat/stat.json")

def load_stat():
    if not STAT_FILE.exists():
        return {"visitors": 0, "buttons": {"sales": 0, "support": 0, "usage": 0, "coverage": 0}}
    with open(STAT_FILE, "r") as f:
        return json.load(f)

def save_stat(stat):
    STAT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STAT_FILE, "w") as f:
        json.dump(stat, f)

def is_bot_running():
    try:
        result = subprocess.run(
            ["systemctl", "is-active", "--quiet", "pondsupportbot.service"],
            check=False
        )
        return result.returncode == 0
    except Exception:
        return False

def increment_button(button_name):
    stat = load_stat()
    if button_name in stat["buttons"]:
        stat["buttons"][button_name] += 1
        save_stat(stat)
