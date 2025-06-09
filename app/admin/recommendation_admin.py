from sqladmin import ModelView

from app.models import Recommendation


class RecommendationAdmin(ModelView, model=Recommendation):
    name_plural = "Рекомендации"
    column_list = [
        Recommendation.content,
        Recommendation.created_at,
    ]
    column_details_list = column_list
    can_export = False
