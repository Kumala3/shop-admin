import logging

import betterlogging as bl
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from bot import bot

app = FastAPI()
    
log_level = logging.INFO
bl.basic_colorized_config(level=log_level)
log = logging.getLogger(__name__)


@app.post("/api")
async def webhook_endpoint(request: Request):
    await bot.send_message(5850071804, "Hello from FastAPI")
    return JSONResponse(status_code=200, content={"status": "ok"})
