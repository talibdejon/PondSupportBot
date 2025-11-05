# health_api.py
from fastapi import FastAPI
import subprocess

app = FastAPI()

def is_bot_running():
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
    if is_bot_running():
        return {"status": "ok"}
    else:
        return {"status": "down"}

