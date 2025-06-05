from datetime import datetime

from pydantic import BaseModel


class EventLogShort(BaseModel):
    event_id: int
    timestamp: datetime
    message: str
    source_ip: str
    user_login: str
    category: str
    severity: str


class EventLogDetails(BaseModel):
    event_id: int
    timestamp: datetime
    source_ip: str
    user_login: str
    message: str
    category: str
    severity: str
    incident_id: int | None
