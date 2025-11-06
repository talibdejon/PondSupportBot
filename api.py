# api.py
from fastapi import FastAPI
import subprocess
import json
from pathlib import Path

app = FastAPI()
STAT_FILE = Path("stat/stat.json")

def load_stat():
    if not STAT_FILE.exists():
        return {"visitors": 0, "buttons": ["sales": 0, "support": 0, "usage": 0, "coverage": 0]}
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

# Endpoints

@app.get("/health")
def health():
    return {"status": "ok"} if is_bot_running() else {"status": "down"}

@app.get("/stat")
def stat():
    stat_data = load_stat()
    return stat_data
