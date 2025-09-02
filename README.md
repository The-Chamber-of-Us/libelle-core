# Libelle Volunteer Intake – MVP

An open-source intake system built by **The Chamber of Us (TCUS)** to onboard volunteers in a simple, trustworthy, and structured way.  

This MVP lets volunteers submit a form with their details and resume. The backend stores resumes in Google Drive, appends structured data to a Google Sheet (our admin view), and runs a parser to extract basic information.

---

## 🚀 Quickstart

### Prerequisites
- Python 3.10+  
- pip / virtualenv  
- Google Cloud service account with access to Sheets & Drive APIs  
- A Google Sheet + Drive folder created for submissions  

### Setup
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
   GOOGLE_SHEET_ID=your-sheet-id
   GOOGLE_DRIVE_FOLDER_ID=your-folder-id
   ```

4. **Run backend**  
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will be live at: `http://localhost:8000`

---

## 📡 API Endpoints
- **POST `/upload`** – Accepts form data + PDF resume.  
- **GET `/healthz`** – Basic health check (Google APIs reachable, parser ready).  

See [`docs/api.md`](./docs/api.md) for details.

---

## 🗄️ Data Flow
- Submissions → Google Sheet (structured data).  
- Resumes → Google Drive (secure folder, private links).  
- Parser extracts text fields (name, email, skills, experience).  
- Admins use Google Sheet as the **only admin view** in MVP.  

For system context, see [`docs/architecture.md`](./docs/architecture.md).

---

## 🔎 Observability
- Upload attempts, parser results, and errors are logged to console/file.  
- Check `/healthz` endpoint for live status.  
- Failed parses still store base info + resume link in Sheet.

---

## 🛠️ Development Notes
- Parser currently supports **text-based PDFs only**.  
- OCR/image-PDF support is a future phase.  
- Contributions welcome — see `CONTRIBUTING.md` (TBD).  

---

## 📬 Contact
Maintainers:  
- Kevin Schmidt – kevin@thechamberofus.org  
- TBD 

---

## 📜 License
AGPL v3.0 – open source, free to use and improve.
