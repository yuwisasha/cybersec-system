from contextlib import contextmanager

from app.core.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
