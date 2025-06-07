from sqladmin import ModelView

from app.models import IncidentRecommendation


class IncidentRecommendationAdmin(ModelView, model=IncidentRecommendation):
    column_list = [
        IncidentRecommendation.incident,
        IncidentRecommendation.recommendation,
        IncidentRecommendation.assigned_at,
        IncidentRecommendation.status,
    ]
    column_details_list = column_list
