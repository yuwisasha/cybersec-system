from sqladmin import ModelView

from app.models import EventLog


class EventLogAdmin(ModelView, model=EventLog):
    name_plural = "Журнал событий"
    column_list = [
        EventLog.event,
        EventLog.user,
        EventLog.category,
        EventLog.severity,
        EventLog.source,
        EventLog.user_login,
        EventLog.source_ip,
        EventLog.message,
    ]
    column_searchable_list = [
        EventLog.user_login,
        EventLog.source_ip,
    ]
    column_details_list = column_list
    can_export = False
