"""Import all routers and add them to routers_list."""
from .admin.admin import admin_router
from .extra.echo import echo_router
from .main.user import user_router

routers_list = [
    admin_router,
    user_router,
    echo_router,  # echo_router must be last
]

__all__ = [
    "routers_list",
]
