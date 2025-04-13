from sqlmodel import create_engine

from app.config import database_settings


engine = create_engine(database_settings.database_url)
