from fastapi import FastAPI
import subprocess
import json
from pathlib import Path

app = FastAPI()

STAT_FILE = Path(__file__).parent / "stat" / "stat.json"

def is_bot_running() -> bool:
    try:
        result = subprocess.run(
            ["systemctl", "is-active", "--quiet", "pondsupportbot.service"],
            check=False
        )
        return result.returncode == 0
    except Exception:
        return False

@app.get("/health")
def health():
    return {"status": "ok"} if is_bot_running() else {"status": "down"}

@app.get("/stat")
def stat():
    try:
        if not STAT_FILE.exists():
            return {"error": "stat.json not found"}
        with open(STAT_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e)}

