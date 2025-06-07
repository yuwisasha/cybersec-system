from sqladmin import ModelView

from app.models import User


class UserAdmin(ModelView, model=User):
    column_list = [
        User.login,
        User.last_name,
        User.first_name,
        User.middle_name,
        User.role,
    ]
    column_searchable_list = [
        User.login,
        User.last_name,
        User.first_name,
        User.middle_name,
    ]
    column_details_list = column_list
