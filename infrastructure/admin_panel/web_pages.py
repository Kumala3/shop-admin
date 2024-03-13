from fastapi import Request
from fastapi.responses import RedirectResponse
from sqladmin import ModelView, action

from infrastructure.database.models.users import User
from infrastructure.database.models.error import Error
from infrastructure.database.models.feature import Feature
from infrastructure.database.models.purchase import Purchase
from infrastructure.database.models.completed_purchase import CompletedPurchase
from infrastructure.admin_panel.utils import format_created_at


class Users(ModelView, model=User):
    @action(
        name="mailing",
        label="Общая Рассылка",
        add_in_list=True,
    )
    async def send_mailing(self, request: Request):
        return RedirectResponse("/action/enter_message")

    column_list = "__all__"
    can_create = False
    can_export = True
    can_edit = True
    can_delete = True
    name_plural = "Пользователи"
    column_formatters = {"created_at": format_created_at}
    column_sortable_list = [User.created_at]
    column_searchable_list = [User.user_id]
    column_default_sort = (User.created_at, True)
    export_types = ["csv", "xls"]
    page_size = 25
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
    column_formatters = {"created_at": format_created_at}
    column_sortable_list = [Feature.created_at]
    column_searchable_list = [Feature.feature_id, Feature.software]
    column_default_sort = (Feature.created_at, True)
    page_size = 25
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
    column_formatters = {"created_at": format_created_at}
    column_sortable_list = [Error.created_at]
    column_searchable_list = [Error.error_id, Error.software]
    column_default_sort = (Error.created_at, True)
    page_size = 25
    column_labels = {
        Error.error_id: "ID пожелания",
        Error.user_id: "ID пользователя",
        Error.software: "Программа",
        Error.created_at: "Дата регистрации сообщения",
        Error.error_message: "Сообщение",
        Error.status: "Статус",
        Error.username: "Никнейм",
    }


class Purchases(ModelView, model=Purchase):
    @action(
        name="mailing",
        label="Общая Рассылка",
        add_in_list=True,
    )
    async def send_mailing(self, request: Request):
        return RedirectResponse("/action/enter_message?customers=true")

    column_list = "__all__"
    can_create = False
    can_export = True
    can_edit = True
    can_delete = True
    name_plural = "Покупки"
    export_types = ["csv", "xls"]
    column_formatters = {"created_at": format_created_at}
    column_sortable_list = [Purchase.created_at]
    column_searchable_list = [Purchase.purchase_id, Purchase.software]
    column_default_sort = (Purchase.created_at, True)
    page_size = 25
    column_labels = {
        Purchase.purchase_id: "ID заказа",
        Purchase.user_id: "ID пользователя",
        Purchase.software: "Программа",
        Purchase.created_at: "Дата регистрации сообщения",
        Purchase.status: "Статус",
        Purchase.username: "Никнейм",
    }


class CompletedPurchases(ModelView, model=CompletedPurchase):
    @action(
        name="mailing",
        label="Рассылка",
        add_in_list=True,
    )
    async def send_mail_to_customers(self, request: Request):
        return RedirectResponse("/action/enter_message?customers=true")

    column_formatters = {"created_at": format_created_at}
    column_list = "__all__"
    can_create = True
    can_export = True
    can_edit = True
    can_delete = True
    name_plural = "Оплаченные покупки"
    export_types = ["csv", "xls"]
    column_sortable_list = [CompletedPurchase.created_at]
    column_searchable_list = [CompletedPurchase.purchase_id, CompletedPurchase.software]
    column_default_sort = (CompletedPurchase.created_at, True)
    page_size = 25
    column_labels = {
        CompletedPurchase.purchase_id: "ID заказа",
        CompletedPurchase.user_id: "ID пользователя",
        CompletedPurchase.software: "Программа",
        CompletedPurchase.created_at: "Дата регистрации сообщения",
        CompletedPurchase.status: "Статус",
        CompletedPurchase.username: "Никнейм",
    }
