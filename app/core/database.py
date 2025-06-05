from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.core.config import settings


engine = create_engine(settings.database_url, echo=False)
SessionLocal = scoped_session(sessionmaker(bind=engine))
