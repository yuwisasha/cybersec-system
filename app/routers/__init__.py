from .ingest import router as ingest_router
from .incidents import router as incedents_router
from .recommendations import router as recommendations_router
from .events import router as events_router
from .auth import router as auth_router

__all__ = (
    "ingest_router",
    "incedents_router",
    "recommendations_router",
    "events_router",
    "auth_router",
)
