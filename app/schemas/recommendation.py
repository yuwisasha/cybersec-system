from pydantic import BaseModel


class RecommendationStatusUpdateRequest(BaseModel):
    status: str
