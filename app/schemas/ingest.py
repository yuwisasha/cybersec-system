from datetime import datetime

from pydantic import BaseModel


class AlertLabels(BaseModel):
    alertname: str
    category: str
    job: str
    service_name: str
    severity: str
    source_type: str
    source_ip: str
    user_login: str


class AlertAnnotations(BaseModel):
    summary: str


class AlertItem(BaseModel):
    annotations: AlertAnnotations
    endsAt: datetime
    startsAt: datetime
    generatorURL: str
    labels: AlertLabels


class EventIngestRequest(BaseModel):
    source_ip: str
    user_login: str | None
    category_id: int
    severity_id: int
    message: str
    timestamp: datetime
