from sqladmin import ModelView

from app.models import Incident


class IncidentAdmin(ModelView, model=Incident):
    name_plural = "Инциденты"
    column_list = [
        Incident.recommendations,
        Incident.created_at,
        Incident.description,
        Incident.status,
    ]
    column_details_list = [
        Incident.recommendations,
        Incident.created_at,
        Incident.description,
        Incident.status,
        Incident.breakdowns,
    ]
    can_export = False
