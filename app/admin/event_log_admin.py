from sqladmin import ModelView

from app.models import EventLog


class EventLogAdmin(ModelView, model=EventLog):
    pass
