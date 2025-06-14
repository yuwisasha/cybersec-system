from fastapi import FastAPI
from sqladmin import Admin

from app.core.database import engine
from app.core.config import settings
from app.routers import (
    ingest_router,
    incedents_router,
    recommendations_router,
    events_router,
    auth_router,
    report_router,
)
from app.admin import (
    UserAdmin,
    EventLogAdmin,
    IncidentRecommendationAdmin,
    IncidentAdmin,
    ReactionRuleAdmin,
    SeverityLevelAdmin,
    RecommendationAdmin,
)
from app.admin.auth_backend import authentication_backend

app = FastAPI(debug=settings.debug)
admin = Admin(app, engine, authentication_backend=authentication_backend)

app.include_router(ingest_router)
app.include_router(incedents_router)
app.include_router(recommendations_router)
app.include_router(events_router)
app.include_router(auth_router)
app.include_router(report_router)

admin.add_model_view(UserAdmin)
admin.add_model_view(EventLogAdmin)
admin.add_model_view(IncidentRecommendationAdmin)
admin.add_model_view(IncidentAdmin)
admin.add_model_view(ReactionRuleAdmin)
admin.add_model_view(SeverityLevelAdmin)
admin.add_model_view(RecommendationAdmin)
