from sqlalchemy import create_engine, Column, Integer, Text, ARRAY, TIMESTAMP, func
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER", "resume_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "resume_pass")
POSTGRES_DB = os.getenv("POSTGRES_DB", "resume_db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

Base = declarative_base()

class Resume(Base):
    __tablename__ = "personal_info"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=True)
    emails = Column(ARRAY(Text), default=[])
    phones = Column(ARRAY(Text), default=[])
    locations = Column(ARRAY(Text), default=[])
    skills = Column(ARRAY(Text), default=[])
    education = Column(ARRAY(Text), default=[])
    work_experience = Column(ARRAY(Text), default=[])
    project_experience = Column(ARRAY(Text), default=[])
    created_at = Column(TIMESTAMP, server_default=func.now())


def ensure_postgres_db():
    """Ensure PostgreSQL user and database exist."""
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=os.getenv("USER"),
            host=POSTGRES_HOST,
            port=POSTGRES_PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        cur.execute(f"SELECT 1 FROM pg_roles WHERE rolname='{POSTGRES_USER}';")
        if not cur.fetchone():
            cur.execute(f"CREATE ROLE {POSTGRES_USER} WITH LOGIN PASSWORD '{POSTGRES_PASSWORD}';")
            print(f"Created user '{POSTGRES_USER}'.")

        cur.execute(f"SELECT 1 FROM pg_database WHERE datname='{POSTGRES_DB}';")
        if not cur.fetchone():
            cur.execute(f"CREATE DATABASE {POSTGRES_DB} OWNER {POSTGRES_USER};")
            print(f"Created database '{POSTGRES_DB}'.")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error ensuring PostgreSQL DB exists: {e}")


def get_engine():
    ensure_postgres_db()
    return create_engine(DATABASE_URL, echo=True)


def get_session_local(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    SessionLocal = get_session_local(engine)
    return engine, SessionLocal


def get_db_session():
    engine, SessionLocal = init_db()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    engine, SessionLocal = init_db()
    print("Database initialized and 'personal_info' table created.")
