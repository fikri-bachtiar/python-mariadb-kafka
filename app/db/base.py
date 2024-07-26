from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

SQLALCHEMY_DATABASE_URL = "mariadb+mariadbconnector://{}:{}@{}:{}/{}".format(
    settings.app_maria_db_username,
    settings.app_maria_db_password,
    settings.app_maria_db_host,
    settings.app_maria_db_port,
    settings.app_maria_db_name,
)

# SQLALCHEMY_DATABASE_URL = "mariadb+mariadbconnector://example_user:example_password@127.0.0.1:3306/example_database"

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
