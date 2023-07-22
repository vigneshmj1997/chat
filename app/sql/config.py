from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager


POSTGRES_HOST = "0.0.0.0"
#POSTGRES_HOST = "172.17.0.1"
POSTGRES_PASSWORD = "7vIA_qTZ_"

HOST = POSTGRES_HOST
PORT = "5432"
USERNAME = "postgres"
PASSWORD = POSTGRES_PASSWORD
DATABASE = "postgres"

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+pg8000://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db_instance():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()