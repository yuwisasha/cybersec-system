from sqladmin import ModelView

from app.models import SeverityLevel


class SeverityLevelAdmin(ModelView, model=SeverityLevel):
    column_list = [
        SeverityLevel.rules,
        SeverityLevel.name,
        SeverityLevel.explanation,
    ]
    column_details_list = [
        SeverityLevel.rules,
        SeverityLevel.name,
        SeverityLevel.explanation,
        SeverityLevel.logs,
    ]
