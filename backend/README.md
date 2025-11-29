# PDF Summarizer Backend (FastAPI)

This is a small, beginner-friendly FastAPI backend that accepts a PDF file, 
extracts its text with PyPDF2, sends the text to Google Gemini (Flash model), 
and returns a clean summary.

## How it works

1. **Upload a PDF**
   - The frontend sends a `POST` request to `/summarize`.
   - The request uses `multipart/form-data` with a field named `file`.

2. **FastAPI endpoint**
   - The `/summarize` endpoint receives the file using `UploadFile`.
   - It checks that the content type is `application/pdf`.

3. **PDF text extraction (PyPDF2)**
   - The file is read into memory.
   - `PyPDF2.PdfReader` opens the PDF from bytes.
   - The code loops over pages (up to 20 pages for this demo) and calls
     `page.extract_text()` to get the text.
   - All page texts are joined into one long string.

4. **Summarization with Gemini (google-generativeai)**
   - The environment variable `GEMINI_API_KEY` is read.
   - `google.generativeai` is configured with this key.
   - A `GenerativeModel("gemini-1.5-flash")` is created.
   - The code sends a prompt like:

     ```python
     response = model.generate_content("Summarize this PDF content..." + text)
     summary = response.text
     ```

   - The summary text is returned to the caller as JSON:

     ```json
     { "summary": "..." }
     ```

5. **CORS**
   - `CORSMiddleware` is enabled with `allow_origins=["*"]` so that the
     static frontend (opened from a file or another origin) can talk to
     this backend.

## Files in this folder

- `main.py` — FastAPI app with the `/summarize` endpoint.
- `utils.py` — Small helper functions:
  - `extract_text_from_pdf` — read PDF bytes and return plain text.
  - `summarize_text_with_gemini` — call Gemini and return the summary.
- `requirements.txt` — Python dependencies for the backend.

## Requirements

Python 3.10+ is recommended.

Backend dependencies (also listed in `requirements.txt`):

```text
fastapi==0.115.0
uvicorn==0.30.1
PyPDF2==3.0.1
google-generativeai==0.8.3
python-multipart==0.0.9
```

## Setup and run locally

1. **Open a terminal inside the `backend` folder**

   ```bash
   cd backend
   ```

2. **Create a virtual environment (optional but recommended)**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # on Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set your Gemini API key**

   You need a Google AI Studio API key.

   On Windows PowerShell, run:

   ```powershell
   setx GEMINI_API_KEY "YOUR_API_KEY_HERE"
   ```

   Then close and reopen the terminal so the variable is available.

5. **Start the FastAPI server with Uvicorn**

   ```bash
   uvicorn main:app --reload
   ```

6. **Test the health endpoint**

   Open:

   - http://127.0.0.1:8000/

   You should see a small JSON message saying the backend is running.

7. **Use with the frontend**

   - Keep the backend running on `http://127.0.0.1:8000`.
   - Open `frontend/index.html` in your browser.
   - Upload a small PDF and click **Summarize**.

## Simple error handling

The backend returns clear error messages in JSON if something goes wrong:

- Wrong file type → `400` with message "Please upload a PDF file."
- No text found → `400` with message "No readable text found in the PDF."
- Missing API key or Gemini error → `500` with a simple message.

These messages are displayed by the frontend under the status area.

## Deployment (Railway example)

Railway is a simple PaaS that can host this FastAPI backend.

### Steps

1. **Push your project to GitHub**
   - Make sure the `backend` folder and `requirements.txt` are included.

2. **Create a new Railway project**
   - Go to https://railway.app
   - Create an account and create a **New Project**.
   - Choose **Deploy from GitHub repo** and select your repository.

3. **Configure the service**
   - When Railway detects Python, set the **Start Command** to:

     ```bash
     uvicorn main:app --host 0.0.0.0 --port $PORT
     ```

   - Set the **Root Directory** to `backend` (if Railway allows this in the
     service settings, so it runs from the backend folder).

4. **Set environment variable**
   - In Railway project settings, add an environment variable:
     - Key: `GEMINI_API_KEY`
     - Value: `YOUR_REAL_API_KEY`

5. **Deploy**
   - Railway will install `requirements.txt` and run your start command.
   - After deployment, it will give you a public URL like:
     - `https://your-app-name.up.railway.app`

6. **Connect the frontend**
   - In `frontend/script.js`, change the backend URL from

     ```js
     fetch("http://127.0.0.1:8000/summarize", {
     ```

     to the Railway URL, for example:

     ```js
     fetch("https://your-app-name.up.railway.app/summarize", {
     ```

   - Then host the `frontend` folder on any static hosting (or simply open the
     `index.html` file locally while testing).

This keeps the backend simple, while still being easy to deploy.
