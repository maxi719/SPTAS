import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


def _database_uri():
    uri = os.getenv("DATABASE_URL", "sqlite:///sptas.db")
    # Render/Heroku-style Postgres URLs may still use the deprecated scheme.
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql+psycopg://", 1)
    return uri


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-only-change-me-too")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)
    SQLALCHEMY_DATABASE_URI = _database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    CORS_ORIGINS = [x.strip() for x in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",") if x.strip()]
    SEED_DEMO_DATA = os.getenv("SEED_DEMO_DATA", "true").lower() == "true"
    DEMO_LECTURER_PASSWORD = os.getenv("DEMO_LECTURER_PASSWORD", "change-me")
