from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_db_app"
SQLALCHEMY_DATABASE_URL = "postgresql://neondb_owner:w6pqxjh2edyA@ep-damp-pine-a293secm-pooler.eu-central-1.aws.neon.tech/neondb?sslmode=require"

engine = create_engine(
  SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()