import logging
import betterlogging as bl

from fastapi import FastAPI
from sqladmin import Admin

from config import load_config, Config

from infrastructure.database.setup import create_engine
from infrastructure.admin_panel.web_pages import Users, Features, Errors, CustomAdmin

config: Config = load_config(".env")
engine = create_engine(config.db)

app = FastAPI()

admin = Admin(
    app,
    engine=engine,
    logo_url=config.admin_panel.logo_url,
)

admin.add_view(Users)
admin.add_view(Features)
admin.add_view(Errors)
admin.add_base_view(CustomAdmin)

log_level = logging.INFO
bl.basic_colorized_config(level=log_level)
log = logging.getLogger(__name__)


@app.get("/test")
async def get_message():
    return {"status": "life - hard, code - easy"}
