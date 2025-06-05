from datetime import date, datetime

from pydantic import BaseModel


class EventLogView(BaseModel):
    event_id: int
    timestamp: datetime
    message: str
    source_ip: str
    user_login: str
    category: str
    severity: str


class RecommendationView(BaseModel):
    id: int
    content: str
    status: str


class IncidentDetailsResponse(BaseModel):
    id: int
    created_at: date
    description: str
    status: str
    events: list[EventLogView]
    recommendations: list[RecommendationView]


class IncidentStatusUpdateRequest(BaseModel):
    status: str


class IncidentListItem(BaseModel):
    id: int
    created_at: date
    description: str
    status: str
    event_count: int
    recommendation_count: int
