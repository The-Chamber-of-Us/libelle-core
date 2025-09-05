from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import fitz  # PyMuPDF
from parser import parse_resume

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the Resume Parser API!"}

@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        contents = await file.read()
        doc = fitz.open(stream=contents, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()

        parsed = parse_resume(text)
        return JSONResponse(content=parsed)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")
