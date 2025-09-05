from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import fitz
import os
from sqlalchemy import create_engine, Column, Integer, Text, ARRAY, TIMESTAMP, func
from sqlalchemy.orm import sessionmaker, declarative_base
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv

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
            print(f"User '{POSTGRES_USER}' created.")

        cur.execute(f"SELECT 1 FROM pg_database WHERE datname='{POSTGRES_DB}';")
        if not cur.fetchone():
            cur.execute(f"CREATE DATABASE {POSTGRES_DB} OWNER {POSTGRES_USER};")
            print(f"Database '{POSTGRES_DB}' created.")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error ensuring PostgreSQL DB exists: {e}")

def get_engine():
    ensure_postgres_db()
    return create_engine(DATABASE_URL, echo=True)

def get_session_local(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)

engine = get_engine()
SessionLocal = get_session_local(engine)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title="Resume Parser API")

@app.post("/upload")
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    try:
        contents = await file.read()
        doc = fitz.open(stream=contents, filetype="pdf")
        text = "".join([page.get_text() for page in doc])
        doc.close()

        from parser import parse_resume 
        parsed = parse_resume(text)

        resume = Resume(
            name=parsed.get("name"),
            emails=parsed.get("emails", []),
            phones=parsed.get("phones", []),
            locations=parsed.get("locations", []),
            skills=parsed.get("skills", []),
            education=parsed.get("education", []),
            work_experience=parsed.get("work_experience", []),
            project_experience=parsed.get("project_experience", []),
        )

        db.add(resume)
        db.commit()
        db.refresh(resume)

        try:
            from sheets_sync import write_resume_to_sheet
            write_resume_to_sheet(resume)
        except ImportError:
            pass

        return JSONResponse(content={"status": "success", "resume_id": resume.id, "parsed": parsed})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")

@app.post("/sheets/webhook")
async def sheets_webhook(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    resume = db.query(Resume).filter(Resume.id == data.get("id")).first()

    if not resume:
        resume = Resume(id=data.get("id"))
        db.add(resume)

    if "name" in data:
        resume.name = data["name"]
    if "emails" in data:
        resume.emails = [email.strip() for email in data["emails"].split(",") if email.strip()]
    if "phones" in data:
        resume.phones = [p.strip() for p in data["phones"].split(",") if p.strip()]
    if "locations" in data:
        resume.locations = [l.strip() for l in data["locations"].split(",") if l.strip()]
    if "skills" in data:
        resume.skills = [s.strip() for s in data["skills"].split(",") if s.strip()]
    if "education" in data:
        resume.education = [e.strip() for e in data["education"].split(",") if e.strip()]
    if "work_experience" in data:
        resume.work_experience = [w.strip() for w in data["work_experience"].split(",") if w.strip()]
    if "project_experience" in data:
        resume.project_experience = [p.strip() for p in data["project_experience"].split(",") if p.strip()]

    db.commit()
    db.refresh(resume)

    try:
        from sheets_sync import update_resume_in_sheet
        update_resume_in_sheet(resume)
    except ImportError:
        pass

    return {"status": "synced", "resume_id": resume.id}

@app.get("/")
def root():
    return {"message": "Resume Parser API is running"}
