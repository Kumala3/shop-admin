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
    """
    View class for managing user data in the admin panel.

    Attributes:
        column_list (str): Specifies the columns to display in the list view.
        can_create (bool): Indicates whether users can create new entries.
        can_export (bool): Indicates whether users can export data.
        can_edit (bool): Indicates whether users can edit existing entries.
        can_delete (bool): Indicates whether users can delete entries.
        name_plural (str): The plural name of the entity being managed.
        column_formatters (dict): Specifies custom formatters for specific columns.
        column_sortable_list (list): Specifies the columns that can be sorted.
        column_searchable_list (list): Specifies the columns that can be searched.
        column_default_sort (tuple): Specifies the default sorting column and order.
        export_types (list): Specifies the available export types.
        page_size (int): Specifies the number of entries to display per page.
        column_labels (dict): Specifies custom labels for specific columns.
    """

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
    """
    Represents a view for managing features in the admin panel.

    Attributes:
        column_list (str): A string specifying the columns to display in the list view.
        can_create (bool): A boolean indicating whether creation of new features is allowed.
        can_export (bool): A boolean indicating whether exporting of features is allowed.
        can_edit (bool): A boolean indicating whether editing of features is allowed.
        can_delete (bool): A boolean indicating whether deletion of features is allowed.
        name_plural (str): A string specifying the plural name for the features.
        export_types (list): A list of strings specifying the export types supported.
        column_formatters (dict): A dictionary mapping column names to formatter functions.
        column_sortable_list (list): A list of columns that can be sorted in the list view.
        column_searchable_list (list): A list of columns that can be searched in the list view.
        column_default_sort (tuple): A tuple specifying the default sort column and order.
        page_size (int): An integer specifying the number of features to display per page.
        column_labels (dict): A dictionary mapping column names to display labels.
    """

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
    """
    View class for managing errors in the admin panel.

    Attributes:
        column_list (str): List of columns to display in the view.
        can_create (bool): Whether creating new errors is allowed.
        can_export (bool): Whether exporting errors is allowed.
        can_edit (bool): Whether editing errors is allowed.
        can_delete (bool): Whether deleting errors is allowed.
        name_plural (str): Plural name for the errors.
        export_types (list): List of export types supported.
        column_formatters (dict): Dictionary of column formatters.
        column_sortable_list (list): List of sortable columns.
        column_searchable_list (list): List of searchable columns.
        column_default_sort (tuple): Default sorting column and order.
        page_size (int): Number of errors to display per page.
        column_labels (dict): Dictionary of column labels.

    """

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
    """
    View class for managing purchases in the admin panel.

    Attributes:
        column_list (list): List of columns to display in the view.
        can_create (bool): Indicates whether new purchases can be created.
        can_export (bool): Indicates whether purchases can be exported.
        can_edit (bool): Indicates whether purchases can be edited.
        can_delete (bool): Indicates whether purchases can be deleted.
        name_plural (str): Plural name for the purchases.
        export_types (list): List of export file types supported.
        column_formatters (dict): Dictionary of column formatters.
        column_sortable_list (list): List of sortable columns.
        column_searchable_list (list): List of searchable columns.
        column_default_sort (tuple): Default column to sort by.
        page_size (int): Number of purchases to display per page.
        column_labels (dict): Dictionary of column labels.

    Methods:
        send_mailing(request: Request) -> RedirectResponse:
            Sends a mailing to all customers and redirects to the message entry page.
    """
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
    """
    Represents a view for managing completed purchases in the admin panel.

    This class provides functionality for sending emails to customers, displaying and managing
    completed purchases, exporting data, and performing CRUD operations.

    Attributes:
        column_formatters (dict): A dictionary mapping column names to formatter functions.
        column_list (str or list): A string or list specifying the columns to display in the view.
        can_create (bool): Indicates whether new completed purchases can be created.
        can_export (bool): Indicates whether data can be exported from the view.
        can_edit (bool): Indicates whether existing completed purchases can be edited.
        can_delete (bool): Indicates whether existing completed purchases can be deleted.
        name_plural (str): The plural name of the view.
        export_types (list): A list of supported export file types.
        column_sortable_list (list): A list of sortable columns.
        column_searchable_list (list): A list of searchable columns.
        column_default_sort (tuple): A tuple specifying the default sort column and order.
        page_size (int): The number of items to display per page.
        column_labels (dict): A dictionary mapping column names to display labels.
    """

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
