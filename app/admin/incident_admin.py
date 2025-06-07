from sqladmin import ModelView

from app.models import Incident


class IncidentAdmin(ModelView, model=Incident):
    column_list = "__all__"
