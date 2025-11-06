# api.py
from fastapi import FastAPI
import utils

@app.get("/health")
def health():
    return {"status": "ok"} if utils.is_bot_running() else {"status": "down"}

@app.get("/stat")
def stat():
    stat_data = utils.load_stat()
    return stat_data
