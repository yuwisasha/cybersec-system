from sqladmin import ModelView

from app.models import ReactionRule


class ReactionRuleAdmin(ModelView, model=ReactionRule):
    column_list = "__all__"
