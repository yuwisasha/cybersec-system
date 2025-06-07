from sqladmin import ModelView

from app.models import SeverityLevel


class SeverityLevelAdmin(ModelView, model=SeverityLevel):
    column_list = "__all__"
