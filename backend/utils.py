"""Utility functions for PDF text extraction and Gemini summarization.

The goal of this file is to keep the logic very simple and easy to read.
"""

import os
from io import BytesIO

from PyPDF2 import PdfReader
import google.generativeai as genai
from fastapi import UploadFile


async def extract_text_from_pdf(upload_file: UploadFile) -> str:
    """Read a PDF upload and return plain text from the first pages.

    This function:
    - reads the uploaded file into memory
    - uses PyPDF2 to extract text from each page
    - limits the number of pages to keep the demo fast
    """

    # Read the file contents into memory (bytes)
    file_bytes = await upload_file.read()

    # Create a file-like object for PyPDF2
    pdf_reader = PdfReader(BytesIO(file_bytes))

    text_parts: list[str] = []
    max_pages = 20  # keep it small so the demo is fast

    for page_index, page in enumerate(pdf_reader.pages):
        if page_index >= max_pages:
            break
        page_text = page.extract_text() or ""
        if page_text.strip():
            text_parts.append(page_text)

    return "\n\n".join(text_parts)


def _get_gemini_model() -> genai.GenerativeModel:
    """Create and return a Gemini model using the API key from the environment.

    The API key must be in the GEMINI_API_KEY environment variable.
    """

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable is not set. "
            "Set it before running the app."
        )

    # Configure the client once per call. For a small demo this is fine.
    genai.configure(api_key=api_key)

    # You can also try "gemini-1.5-flash-002" or "gemini-2.0-flash" if available
    # return genai.GenerativeModel("gemini-1.5-flash")
    return genai.GenerativeModel("gemini-2.0-flash")


def summarize_text_with_gemini(text: str, prompt_type: str = "medium", custom_prompt: str = None) -> str:
    """Send text to Gemini and return a summary with the specified prompt type.
    
    Args:
        text: The text to summarize
        prompt_type: One of 'short', 'medium', 'long', or 'custom'
        custom_prompt: Custom prompt to use if prompt_type is 'custom'
    """
    if not text.strip():
        raise ValueError("No text provided for summarization.")

    # Limit the number of characters to keep the request small.
    max_chars = 8000
    if len(text) > max_chars:
        text = text[:max_chars]

    model = _get_gemini_model()

    # Define different prompt templates
    prompt_templates = {
        "short": "Provide a very brief summary (2-3 sentences) of this text:",
        "medium": "Summarize this content in clear, simple English. Use short paragraphs and bullet points if helpful:",
        "long": "Provide a detailed summary of this content, covering all key points. Use clear section headers and bullet points:"
    }

    # Select or use custom prompt
    if prompt_type == "custom" and custom_prompt:
        prompt = f"{custom_prompt}\n\n{text}"
    else:
        prompt = f"{prompt_templates.get(prompt_type, prompt_templates['medium'])}\n\n{text}"

    # Call the Gemini API
    response = model.generate_content(prompt)
    summary = (response.text or "").strip()
    
    if not summary:
        raise ValueError("Gemini did not return any summary text.")

    return summary
