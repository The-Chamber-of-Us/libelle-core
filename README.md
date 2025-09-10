# Libelle Volunteer Intake – MVP

An open-source intake system built by The Chamber of Us (TCUS) to onboard volunteers in a simple, trustworthy, and structured way.

This MVP lets volunteers submit a form with their details and resume. The backend stores resumes in Google Drive, appends structured data to a Google Sheet (our admin view), and runs a parser to extract basic information.

---

## 🚀 Quickstart

### Prerequisites
- Python 3.10+
- `pip` or `virtualenv`
- Google Cloud service account with access to Sheets & Drive APIs
- A Google Sheet and Drive folder created for submissions

---

### 🔧 Setup

1. **Clone repo**
```bash
git clone https://github.com/thechamberofus/libelle.git
cd libelle
```

2. **Create virtual environment & install dependencies**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Configure environment variables**

Create a `.env` file in the project root with:
```
GOOGLE_SERVICE_ACCOUNT_KEY=path/to/key.json
GOOGLE_SHEET_ID=your-google-sheet-id
GOOGLE_DRIVE_FOLDER_ID=your-drive-folder-id
```

4. **Run the backend**
```bash
uvicorn app.main:app --reload
```

The API will be live at: [http://localhost:8000](http://localhost:8000)

---

## 📡 API Endpoints

### `POST /upload`
Accepts:
- Form fields: `name`, `email`, etc.
- File upload: `resume` (PDF only)

Stores:
- Resume in Google Drive
- Structured info in Google Sheet

Returns `200 OK` on success, error codes on failure.

### `GET /healthz`
Returns basic status of:
- Google API connectivity
- Parser health

Use this to check if system is ready for uploads.

---

## 🗄️ Data Flow

- Submissions → Google Sheet (structured data)
- Resumes → Google Drive (secure folder, private links)
- Parser extracts:
  - Name
  - Email
  - Skills
  - Experience (limited for now)

Admin view is just the Google Sheet.

---

## 🔎 Observability

- Console/file logs include:
  - Upload attempts
  - Parser results
  - Errors
- `/healthz` reports backend health
- If parsing fails, the resume is still saved, and a base record is written

---

## 🛠️ Development Notes

- Parser supports text-based PDFs only (no OCR yet)
- Frontend should use proper CORS headers when calling backend
- `.env` and credentials should never be committed
- OCR/image-PDF support may come in future releases

---

## 📬 Maintainers

- Kevin Schmidt – kevin@thechamberofus.org
- TBD

---
