from fastapi import FastAPI, UploadFile, File
from pathlib import Path
import shutil

from app.parser import extract_text_from_pdf


app = FastAPI(
    title="Drishti-Scribe API",
    description="Backend for accessible document understanding",
    version="0.1.0"
)


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/")
def root():
    return {
        "message": "Drishti-Scribe API is running"
    }


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        return {
            "error": "Only PDF files are supported"
        }

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    pages = extract_text_from_pdf(str(file_path))

    return {
        "filename": file.filename,
        "pages": pages
    }