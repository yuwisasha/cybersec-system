from sqladmin import ModelView

from app.models import User


class UserAdmin(ModelView, model=User):
    column_list = "__all__"
