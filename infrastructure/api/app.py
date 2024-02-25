import logging
import betterlogging as bl

from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import BackgroundTasks
from sqladmin import Admin

from config import load_config, Config

from infrastructure.database.setup import create_engine
from infrastructure.admin_panel.web_pages import Users, Features, Errors
from infrastructure.admin_panel.authentication import AdminAuth
from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.api.utils import get_repo
from bot import bot

config: Config = load_config(".env")
engine = create_engine(config.db)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

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


log_level = logging.INFO
bl.basic_colorized_config(level=log_level)
log = logging.getLogger(__name__)

templates = Jinja2Templates(directory="templates")


@app.get("/api")
async def webhook_endpoint(request: Request):
    await bot.send_message(5850071804, "Hello from FastAPI")
    return JSONResponse(status_code=200, content={"status": "ok"})


@app.get("/action/enter_message", response_class=HTMLResponse)
async def enter_message(request: Request):
    return templates.TemplateResponse("message.html", {"request": request})


@app.post("/submit_message", response_class=HTMLResponse)
async def start_mailing(
    request: Request,
    background_tasks: BackgroundTasks,
    repo: RequestsRepo = Depends(get_repo),
):
    raw_text = await request.form()
    formatted_message = str(raw_text["message"].strip())

    all_users = await repo.users.get_all_users()

    async def send_messages(message: str, users: list):
        for user in users:
            try:
                await bot.send_message(
                    user.user_id, text=message, disable_web_page_preview=True
                )
            except Exception as e:
                log.info(f"Error sending message to user {user.user_id}: {e}")
        log.info(f"Mailing was successful for {len(users)} users")

    background_tasks.add_task(send_messages, formatted_message, all_users)

    return templates.TemplateResponse(
        "success_mailing.html", {"request": request, "count_users": len(all_users)}
    )
