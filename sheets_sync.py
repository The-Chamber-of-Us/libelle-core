import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
from main import Resume

GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS", "credentials.json")
SHEET_NAME = "Resumes"

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = service_account.Credentials.from_service_account_file(
    GOOGLE_CREDENTIALS, scopes=SCOPES
)

service = build("sheets", "v4", credentials=creds)
sheet = service.spreadsheets()

def resume_to_row(resume: Resume):
    return [
        resume.id,
        resume.name,
        ", ".join(resume.emails or []),
        ", ".join(resume.phones or []),
        ", ".join(resume.locations or []),
        ", ".join(resume.skills or []),
        ", ".join(resume.education or []),
        ", ".join(resume.work_experience or []),
        ", ".join(resume.project_experience or []),
    ]

def write_resume_to_sheet(resume: Resume):
    body = {"values": [resume_to_row(resume)]}
    sheet.values().append(
        spreadsheetId=GOOGLE_SHEET_ID,
        range=f"{SHEET_NAME}!A2",
        valueInputOption="RAW",
        body=body,
    ).execute()

def update_resume_in_sheet(resume: Resume):
    values = sheet.values().get(
        spreadsheetId=GOOGLE_SHEET_ID, range=f"{SHEET_NAME}!A2:A"
    ).execute()
    ids = [row[0] for row in values.get("values", []) if row]

    if str(resume.id) in ids:
        row_index = ids.index(str(resume.id)) + 2
        body = {"values": [resume_to_row(resume)]}
        sheet.values().update(
            spreadsheetId=GOOGLE_SHEET_ID,
            range=f"{SHEET_NAME}!A{row_index}",
            valueInputOption="RAW",
            body=body,
        ).execute()
    else:
        write_resume_to_sheet(resume)
