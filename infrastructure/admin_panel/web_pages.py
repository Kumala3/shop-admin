from fastapi import Request
from sqladmin import ModelView, BaseView, expose
from infrastructure.database.models.users import User
from infrastructure.database.models.error import Error
from infrastructure.database.models.feature import Feature


class Users(ModelView, model=User):
    column_list = "__all__"
    can_create = False
    can_export = True
    can_edit = True
    can_delete = True
    name_plural = "Пользователи"
    column_sortable_list = [User.created_at]
    column_searchable_list = [User.user_id]
    export_types = ["csv", "xls"]
    column_labels = {
        User.created_at: "Дата регистрации",
        User.user_id: "ID пользователя",
        User.username: "Никнейм",
        User.full_name: "Полное имя",
        User.language_code: "Язык",
        User.is_premium: "Премиум",
        User.is_bot: "Бот",
    }


class Features(ModelView, model=Feature):
    column_list = "__all__"
    can_create = False
    can_export = True
    can_edit = True
    can_delete = True
    name_plural = "Пожелания"
    export_types = ["csv", "xls"]
    column_sortable_list = [Feature.created_at]
    column_searchable_list = [Feature.feature_id, Feature.software]
    column_labels = {
        Feature.feature_id: "ID пожелания",
        Feature.user_id: "ID пользователя",
        Feature.software: "Программа",
        Feature.created_at: "Дата регистрации сообщения",
        Feature.feature_message: "Сообщение",
        Feature.status: "Статус",
        Feature.username: "Никнейм",
    }


class Errors(ModelView, model=Error):
    column_list = "__all__"
    can_create = False
    can_export = True
    can_edit = True
    can_delete = True
    name_plural = "Ошибки"
    export_types = ["csv", "xls"]
    column_sortable_list = [Error.created_at]
    column_searchable_list = [Error.error_id, Error.software]
    column_labels = {
        Error.error_id: "ID пожелания",
        Error.user_id: "ID пользователя",
        Error.software: "Программа",
        Error.created_at: "Дата регистрации сообщения",
        Error.error_message: "Сообщение",
        Error.status: "Статус",
        Error.username: "Никнейм",
    }


class CustomAdmin(BaseView):
    name = "Custom Page"
    icon = ""

    @expose("/custom", methods=["GET"])
    async def test_page(self, request: Request):
        # return await self.templates.TemplateResponse(request, "custom.html")
        return {"status": "life - hard, code - easy"}
