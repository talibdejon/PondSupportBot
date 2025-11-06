# api.py
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import utils

app = FastAPI()

@app.api_route("/health", methods=["GET", "HEAD"])
def health():
    if utils.is_bot_running():
        return JSONResponse(content={"status": "up"}, status_code=200)
    else:
        return JSONResponse(content={"status": "down"}, status_code=503)

@app.get("/stat")
def stat():
    stat_data = utils.load_stat()
    return stat_data
