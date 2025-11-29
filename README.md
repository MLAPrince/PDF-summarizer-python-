# PDF Summarizer - Documentation

## Overview
PDF Summarizer is a web application that allows users to upload PDF files and generate concise summaries using Google's Gemini AI. The application offers multiple summary types and supports custom prompts for tailored summarization.

## Features

### 1. Multiple Summary Types
- **Short**: Brief 2-3 sentence summary
- **Medium**: Standard summary with key points
- **Long**: Detailed summary with section headers
- **Custom**: User-defined prompt for personalized summarization

### 2. User-Friendly Interface
- Clean, responsive design
- Intuitive file upload
- Real-time status updates
- Error handling with helpful messages

## Technical Stack

### Backend (FastAPI)
- **Framework**: FastAPI
- **Dependencies**:
  - `fastapi`: Web framework
  - `uvicorn`: ASGI server
  - `python-multipart`: File upload handling
  - `PyPDF2`: PDF text extraction
  - `google-generativeai`: Gemini AI integration
  - `python-dotenv`: Environment variable management

### Frontend
- **HTML5**: Structure
- **CSS3**: Styling
- **JavaScript**: Client-side functionality

## Installation

### Prerequisites
- Python 3.8+
- Node.js (for frontend development)
- Google Gemini API key

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd pdf_summarizer
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Create a `.env` file in the `backend` directory:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

4. **Run the backend server**
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`

5. **Open the frontend**
   - Open `frontend/index.html` in a web browser
   - Or use a local server (e.g., `python -m http.server` in the frontend directory)

## API Endpoints

### POST /summarize
Upload a PDF file and get a summary.

**Request**
- **Method**: POST
- **Content-Type**: multipart/form-data
- **Parameters**:
  - `file` (required): PDF file to summarize
  - `prompt_type` (optional): Type of summary (`short`, `medium`, `long`, `custom`)
  - `custom_prompt` (optional): Custom prompt text (required if `prompt_type` is `custom`)

**Response**
```json
{
    "summary": "Generated summary text..."
}
```

## Error Handling

### Common Error Responses
- `400 Bad Request`: Invalid file type or missing required fields
- `500 Internal Server Error`: Server-side error during processing

## Usage Guide

### Generating a Summary
1. Open the application in your web browser
2. Click "Choose a PDF file" and select your PDF
3. Select a summary type (Short, Medium, Long, or Custom)
4. If using Custom, enter your prompt in the text area
5. Click "Generate Summary"
6. View the generated summary in the results area

### Tips for Best Results
- For technical documents, use the "Long" summary type
- For quick overviews, use the "Short" summary type
- When using custom prompts, be specific about the information you want highlighted
- Keep custom prompts concise but clear

## Troubleshooting

### Common Issues
1. **File not uploading**
   - Ensure the file is a valid PDF
   - Check file size (large files may take longer to process)

2. **API Key not found**
   - Verify the `.env` file exists in the backend directory
   - Ensure the `GEMINI_API_KEY` is set correctly

3. **Server not responding**
   - Check if the backend server is running
   - Verify the server address in the frontend JavaScript matches the backend URL

## Security Considerations
- API keys should never be committed to version control
- The application processes files on the server; ensure proper security measures are in place in production
- Consider implementing rate limiting for production use

## License
[Specify your license here]

## Contributing
[Your contribution guidelines here]

## Support
For support, please contact [your contact information]
