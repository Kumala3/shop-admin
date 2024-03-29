import logging
import betterlogging as bl
from typing import Optional
import shutil

from fastapi import FastAPI, Request, Depends, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import BackgroundTasks
from sqladmin import Admin

from config import load_config, Config

from infrastructure.database.setup import create_engine
from infrastructure.admin_panel.web_pages import (
    Users,
    Features,
    Errors,
    Purchases,
    CompletedPurchases,
)
from infrastructure.admin_panel.authentication import AdminAuth
from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.api.utils import get_repo, send_file, send_message
from bot import bot
from aiogram.types import URLInputFile

config: Config = load_config(".env")
engine = create_engine(config.db)

app = FastAPI()
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")


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
admin.add_view(Purchases)
admin.add_view(CompletedPurchases)


log_level = logging.INFO
bl.basic_colorized_config(level=log_level)
log = logging.getLogger(__name__)

templates = Jinja2Templates(directory="frontend/templates")


@app.get("/api")
async def webhook_endpoint(request: Request):
    await bot.send_message(5850071804, "Hello from FastAPI")
    return JSONResponse(status_code=200, content={"status": "ok"})


@app.get("/action/enter_message", response_class=HTMLResponse)
async def enter_message(request: Request):
    is_customers = request.query_params.get("customers")
    return templates.TemplateResponse(
        "message.html", {"request": request, "only_customers": is_customers}
    )


@app.post("/submit_message", response_class=HTMLResponse)
async def start_mailing(
    request: Request,
    background_tasks: BackgroundTasks,
    upload_file: Optional[UploadFile] = None,
    repo: RequestsRepo = Depends(get_repo),
):
    raw_text = await request.form()
    formatted_message = str(raw_text["message"].strip())

    status = request.query_params.get("customers")

    customers_ids = await repo.completed_purchases.get_customers_ids()

    users_ids = await repo.users.get_users_ids()

    # Check if the admin uploaded any file
    if upload_file.filename != "":
        temp_file_path = f"temp_{upload_file.filename}"

        try:
            # Download the file to the file system
            with open(temp_file_path, "wb") as temp_file:
                shutil.copyfileobj(upload_file.file, temp_file)
        except Exception as e:
            log.info(f"There was an error during downloading file: {e}")

    # If the admin wants to send a message to customers
    if status == "true":
        try:
            # If there's no file, send simple message without any attachments
            if upload_file.filename == "":
                background_tasks.add_task(
                    send_message, formatted_message, customers_ids
                )
            else:
                background_tasks.add_task(
                    send_file, customers_ids, formatted_message, temp_file_path
                )
            return templates.TemplateResponse(
                "success_mailing.html",
                {"request": request, "count_users": len(customers_ids)},
            )
        except Exception as e:
            log.info(f"Error sending message to customers: {e}")
            return JSONResponse(
                status_code=500, content={"error": "Internal Server Error"}
            )
    # If the admin wants to send a message to all users
    else:
        try:
            if upload_file.filename == "":
                background_tasks.add_task(send_message, formatted_message, users_ids)
            else:
                background_tasks.add_task(
                    send_file, users_ids, formatted_message, temp_file_path
                )
            return templates.TemplateResponse(
                "success_mailing.html",
                {"request": request, "count_users": len(users_ids)},
            )
        except Exception as e:
            log.info(f"There was an error during sending message or file: {e}")
            return JSONResponse(
                status_code=500, content={"error": "Internal Server Error"}
            )


@app.post("/payment_aaio")
async def aaio_handler(request: Request, repo: RequestsRepo = Depends(get_repo)):
    data = await request.form()
    status = data["status"]

    purchase_id = data["order_id"]

    purchase = await repo.purchases.get_purchase_by_id(int(purchase_id))

    await repo.completed_purchases.create_completed_order(purchase=purchase)
    await repo.purchases.delete_purchase_by_id(int(purchase_id))

    if status == "success":
        photo = URLInputFile(
            "https://drive.usercontent.google.com/download?id=1ZSx7ffkDGUBnBlme9I6ALVGYJxLLNH_1&export=download"
        )
        desc = data["desc"]
        data = desc.split("|")

        if "19.4" in data[1]:
            file = URLInputFile(
                "https://drive.usercontent.google.com/download?id=1n9-4qrc6t4scS19HIVb_QLQ6wLYeYsGH&export=download",
                filename="SeoSpider_RU19.4.properties",
            )
            await bot.send_photo(
                int(data[2]),
                caption="Инструкция по установке перевода:\n1. Скачайте файл с переводом ниже;\n2. Закройте программу (если сейчас открыта);\n3. Измените название скачанного файла таким образом, чтобы он назывался «SeoSpider_ru»;\n4. Откройте папку «translations» где установлена программа, как правило дефолтные значения будут такие: C:\Program Files (x86)\Screaming Frog SEO Spider\ScreamingFrogSEOSpider\translations;\n5. Добавьте в архив скачанный файл;\n6. Запустите программу;",
                photo=photo,
            )
            await bot.send_document((data[2]), file)
        elif "19.2" in data[1]:
            file = URLInputFile(
                "https://drive.usercontent.google.com/download?id=1iH8s9g7a9HfbgpquOkpTDKrkPRJ40SQl&export=download",
                filename="SeoSpider_RU19.2.properties",
            )
            await bot.send_photo(
                int(data[2]),
                caption="Инструкция по установке перевода:\n1. Скачайте файл с переводом ниже;\n2. Закройте программу (если сейчас открыта);\n3. Измените название скачанного файла таким образом, чтобы он назывался «SeoSpider_ru»;\n4. Откройте папку «translations» где установлена программа, как правило дефолтные значения будут такие: C:\Program Files (x86)\Screaming Frog SEO Spider\ScreamingFrogSEOSpider\translations;\n5. Добавьте в архив скачанный файл;\n6. Запустите программу;",
                photo=photo,
            )
            await bot.send_document((data[2]), file)
        elif "6.0" in data[1]:
            file = URLInputFile(
                "https://drive.usercontent.google.com/download?id=1ZX4_IKy1H9pyvJ8Ss9NAlAdZMEsswgvU&export=download",
                filename="SeoSpider_EN6.0.properties",
            )
            await bot.send_photo(
                int(data[2]),
                caption="Инструкция по установке перевода:\n1. Скачайте файл с переводом ниже;\n2. Закройте программу (если сейчас открыта);\n3. Измените название скачанного файла таким образом, чтобы он назывался «LogFileAnalyser_en»;\n3. Откройте папку «translations» где установлена программа, как правило дефолтные значения будут такие: C:\Program Files (x86)\Screaming Frog Log File Analyser\ScreamingFrogLogFileAnalyser\translations;\n4. Сохраните где-нибудь исходный файл «LogFileAnalyser_en» на всякий случай;\n5. Замените текущий файл на скачанный;\n6. Запустите программу;",
                photo=photo,
            )
            await bot.send_document((data[2]), file)
        elif "5.3" in data[1]:
            file = URLInputFile(
                "https://drive.usercontent.google.com/download?id=1TJSAYj_NB9f6tU_cLn2vCKIxUfGlzI0M&export=download",
                filename="SeoSpider_EN5.3.properties",
            )
            await bot.send_photo(
                int(data[2]),
                caption="Инструкция по установке перевода:\n1. Скачайте файл с переводом ниже;\n2. Закройте программу (если сейчас открыта);\n3. Измените название скачанного файла таким образом, чтобы он назывался «LogFileAnalyser_en»;\n3. Откройте папку «translations» где установлена программа, как правило дефолтные значения будут такие: C:\Program Files (x86)\Screaming Frog Log File Analyser\ScreamingFrogLogFileAnalyser\translations;\n4. Сохраните где-нибудь исходный файл «LogFileAnalyser_en» на всякий случай;\n5. Замените текущий файл на скачанный;\n6. Запустите программу;",
                photo=photo,
            )
            await bot.send_document((data[2]), file)
