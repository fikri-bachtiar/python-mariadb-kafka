from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

SQLALCHEMY_DATABASE_URL = "mariadb+mariadbconnector://{}:{}@{}:{}/{}".format(
    settings.app_maria_db_username,
    settings.app_maria_db_password,
    settings.app_maria_db_host,
    settings.app_maria_db_port,
    settings.app_maria_db_name,
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
