# Simple PDF Summarizer (FastAPI + Gemini)

A beginner-friendly project that lets you upload a small PDF, summarizes it
using Google Gemini (Flash model), and shows the summary in the browser.

- **Backend:** Python, FastAPI, PyPDF2, google-generativeai, Uvicorn
- **Frontend:** Plain HTML, CSS, and JavaScript (no frameworks)
- **Storage:** None (everything is processed in memory)

---

## Project structure

```text
pdf_summarizer/
│── backend/
│   ├── main.py          # FastAPI app and /summarize endpoint
│   ├── utils.py         # Small helper functions
│   ├── requirements.txt # Backend dependencies
│   └── README.md        # Backend details and deployment notes
│
│── frontend/
│   ├── index.html       # Simple upload page
│   ├── script.js        # Calls the backend and shows the summary
│   └── style.css        # Basic styling
│
└── README.md            # You are here (project overview)
```

---

## What the app does

1. You open the frontend page.
2. You select a PDF file (10–20 pages for demo is ideal).
3. The browser sends the file to the FastAPI backend.
4. The backend:
   - reads the PDF in memory
   - extracts text with PyPDF2
   - sends the text to Gemini Flash via `google.generativeai`
   - returns a clean summary as JSON
5. The frontend displays the summary on the page.

Everything runs in memory. No files are stored on disk or in a database.

---

## How the backend works (high-level)

- `main.py`
  - defines a FastAPI app
  - adds CORS middleware so the frontend can call it
  - exposes a `POST /summarize` endpoint that accepts `UploadFile`

- `utils.py`
  - `extract_text_from_pdf(upload_file)`
    - reads the uploaded file bytes
    - uses `PyPDF2.PdfReader` to read up to 20 pages
    - joins all extracted text into one string
  - `summarize_text_with_gemini(text)`
    - configures `google.generativeai` using `GEMINI_API_KEY`
    - creates a `GenerativeModel("gemini-1.5-flash")`
    - calls `model.generate_content("Summarize this: " + text)`
    - returns `response.text` as the summary

The code is intentionally simple: small functions, few dependencies, and
straightforward control flow.

---

## How the frontend works (high-level)

- `index.html`
  - simple page with a file input and a **Summarize** button
  - an empty `<div>` where the summary will appear

- `script.js`
  - listens to the form `submit` event
  - builds a `FormData` object with the selected file as `file`
  - sends a `fetch` `POST` request to `http://127.0.0.1:8000/summarize`
  - reads the JSON response and puts `data.summary` into the summary `<div>`
  - shows basic status messages and errors

- `style.css`
  - adds light styling so the page looks clean and readable

---

## Running the project locally

### 1. Start the backend

1. Open a terminal in the `backend` folder:

   ```bash
   cd backend
   ```

2. (Optional) Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set your Gemini API key (Windows PowerShell example):

   ```powershell
   setx GEMINI_API_KEY "YOUR_API_KEY_HERE"
   ```

   Close and reopen the terminal so the environment variable is loaded.

5. Start the server:

   ```bash
   uvicorn main:app --reload
   ```

6. Verify it is running:
   - Open: http://127.0.0.1:8000/

### 2. Open the frontend

1. Open the `frontend/index.html` file in your browser.
   - You can usually double-click it, or use **Open With → Browser**.

2. Make sure the backend is running on `http://127.0.0.1:8000`.

3. On the page:
   - Choose a small PDF file.
   - Click **Summarize**.
   - Wait for the summary to appear.

If you see a message about not reaching the backend, check that Uvicorn is
still running and that there are no errors in its terminal.

---

## Deployment overview

There are many ways to deploy this project. Here are two simple options.

### Option 1: Railway (recommended for beginners)

1. Put this `pdf_summarizer` project in a GitHub repo.
2. Go to https://railway.app and create a new project.
3. Connect your GitHub repo and choose it for deployment.
4. In the service settings:
   - Set **Root Directory** to `backend` (so it uses the backend folder).
   - Set the **Start Command** to:

     ```bash
     uvicorn main:app --host 0.0.0.0 --port $PORT
     ```

   - Add an environment variable:
     - Key: `GEMINI_API_KEY`
     - Value: your actual Gemini API key.

5. Deploy. Railway will install `requirements.txt` and run the server.
6. After deploy, Railway gives you a URL like
   `https://your-app-name.up.railway.app`.
7. Update `frontend/script.js` so `fetch` points to your Railway URL.
8. Host the `frontend` folder as static files (or open `index.html` locally
   to test hitting the Railway backend).

### Option 2: Vercel (serverless function)

Vercel is great for static frontends but can also run small Python
serverless functions.

A simple approach:

1. Host only the `frontend` folder on Vercel (very easy).
2. Deploy the FastAPI backend on Railway or another service.
3. Point the frontend `fetch` URL to that backend.

This keeps the setup simple and avoids complex serverless FastAPI configs.

---

## Example screenshots (placeholders)

You can add screenshots here later, for example:

- `screenshots/upload-page.png` — the upload page with a file selected.
- `screenshots/summary-result.png` — the page showing a generated summary.

In a real project, you would commit PNG files and reference them here.

---

This project is designed so a beginner can explain it in an interview:
- clear folder structure
- small functions
- straightforward API call to Gemini
- easy local run and deployment story.
