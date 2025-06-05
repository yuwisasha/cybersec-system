from fastapi import FastAPI

from app.core.config import settings
from app.routers import (
    ingest_router,
    incedents_router,
    recommendations_router,
    events_router,
)

app = FastAPI(debug=settings.debug)

app.include_router(ingest_router)
app.include_router(incedents_router)
app.include_router(recommendations_router)
app.include_router(events_router)
