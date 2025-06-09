from sqladmin import ModelView

from app.models import IncidentRecommendation


class IncidentRecommendationAdmin(ModelView, model=IncidentRecommendation):
    name_plural = "Рекомендации к инцидентам"
    column_list = [
        IncidentRecommendation.incident,
        IncidentRecommendation.recommendation,
        IncidentRecommendation.assigned_at,
        IncidentRecommendation.status,
    ]
    column_details_list = column_list
    list_template = "sqladmin/custom_list.html"
