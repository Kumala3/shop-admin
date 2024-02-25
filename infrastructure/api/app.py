import logging
import betterlogging as bl

from fastapi import FastAPI, Request
from sqladmin import Admin

from config import load_config, Config

from infrastructure.database.setup import create_engine
from infrastructure.admin_panel.web_pages import Users, Features, Errors
from infrastructure.admin_panel.authentication import AdminAuth
from bot import bot

config: Config = load_config(".env")
engine = create_engine(config.db)

app = FastAPI()

authentication_backend = AdminAuth(
    secret_key=config.admin_panel.secret_key,
)

admin = Admin(
    app,
    engine=engine,
    logo_url=config.admin_panel.logo_url,
    authentication_backend=authentication_backend,
)

admin.add_view(Users)
admin.add_view(Features)
admin.add_view(Errors)
# admin.add_base_view(CustomAdmin)

    
log_level = logging.INFO
bl.basic_colorized_config(level=log_level)
log = logging.getLogger(__name__)


@app.post("/api")
async def webhook_endpoint(request: Request):
    await bot.send_message(5850071804, "Hello from FastAPI")
    return JSONResponse(status_code=200, content={"status": "ok"})
