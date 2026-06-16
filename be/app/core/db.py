import uuid
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import QueuePool
from sqlmodel import Session, create_engine
from app.core.config import settings

engine = create_engine(
	str(settings.SQLALCHEMY_DATABASE_URI),
	poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_recycle=1800,
    pool_timeout=30,
    pool_pre_ping=True,
)
Base = declarative_base()
# Don't call create_all here - use Alembic migrations instead

def get_db():
    with Session(engine) as session:
        session.session_id = str(uuid.uuid4())  # type: ignore
        yield session
