from sqladmin import ModelView

from app.models import IncidentRecommendation


class IncidentRecommendationAdmin(ModelView, model=IncidentRecommendation):
    column_list = "__all__"
