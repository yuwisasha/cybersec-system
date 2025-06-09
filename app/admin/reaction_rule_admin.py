from sqladmin import ModelView

from app.models import ReactionRule


class ReactionRuleAdmin(ModelView, model=ReactionRule):
    name_plural = "Правила реагирования"
    column_list = [
        ReactionRule.severity,
        ReactionRule.recommendation,
        ReactionRule.source_type,
    ]
    column_details_list = column_list
    can_export = False
