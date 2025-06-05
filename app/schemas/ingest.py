from datetime import datetime

from pydantic import BaseModel


class EventIngestRequest(BaseModel):
    source_ip: str
    user_login: str
    category_id: int
    severity_id: int
    message: str
    timestamp: datetime
