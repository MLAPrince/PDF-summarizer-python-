"""Simple FastAPI backend for a PDF summarizer.

This app exposes one endpoint:
- POST /summarize : upload a PDF and get a summary from Gemini
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from utils import extract_text_from_pdf, summarize_text_with_gemini


app = FastAPI(title="PDF Summarizer API")

# Allow calls from any origin (good for local testing with a static HTML file)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> dict:
    """Small health check endpoint."""

    return {"message": "PDF Summarizer backend is running."}


from pydantic import BaseModel
from typing import Optional

class SummaryRequest(BaseModel):
    prompt_type: str = "medium"
    custom_prompt: Optional[str] = None

from fastapi import Form

@app.post("/summarize")
async def summarize(
    file: UploadFile = File(...),
    prompt_type: str = Form("medium"),
    custom_prompt: Optional[str] = Form(None)
) -> dict:
    """Accept a PDF file upload and return a summary with the specified prompt type.
    
    Args:
        file: The uploaded PDF file
        prompt_type: Type of summary to generate (short/medium/long/custom)
        custom_prompt: Custom prompt to use if prompt_type is 'custom'
    """
    # Debug log the received form data
    print(f"Received request with prompt_type: {prompt_type}")
    if custom_prompt:
        print(f"Custom prompt: {custom_prompt[:100]}...")  # Print first 100 chars

    # Basic validation: only accept PDFs
    if not file.content_type or "pdf" not in file.content_type.lower():
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")

    try:
        # Extract text using PyPDF2 (via our helper function)
        text = await extract_text_from_pdf(file)
    except Exception as exc:
        print(f"Error extracting text from PDF: {str(exc)}")
        raise HTTPException(status_code=500, detail=f"Could not read PDF: {exc}")

    if not text.strip():
        raise HTTPException(status_code=400, detail="No readable text found in the PDF.")

    # Validate prompt_type
    valid_prompt_types = ["short", "medium", "long", "custom"]
    if prompt_type not in valid_prompt_types:
        print(f"Invalid prompt_type: {prompt_type}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid prompt_type. Must be one of: {', '.join(valid_prompt_types)}"
        )

    # If custom prompt is selected but not provided
    if prompt_type == "custom" and not custom_prompt:
        print("Custom prompt is required but not provided")
        raise HTTPException(
            status_code=400,
            detail="Custom prompt is required when prompt_type is 'custom'"
        )

    try:
        print(f"Generating summary with prompt_type: {prompt_type}")
        # Send the text to Gemini and get a summary
        summary = summarize_text_with_gemini(
            text,
            prompt_type=prompt_type,
            custom_prompt=custom_prompt
        )
        return {"summary": summary}
    except ValueError as exc:
        # Errors we raised on purpose (for example missing API key)
        print(f"ValueError in summarize_text_with_gemini: {str(exc)}")
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        print(f"Unexpected error in summarize_text_with_gemini: {str(exc)}")
        raise HTTPException(
            status_code=500,
            detail=f"Something went wrong while calling the Gemini API: {str(exc)}",
        )
