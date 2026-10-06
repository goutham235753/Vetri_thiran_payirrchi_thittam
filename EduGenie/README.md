# EduGenie — Google Gemini Powered Learning Assistant

This complete implementation follows the supplied EduGenie document: FastAPI backend, HTML/CSS frontend, Q&A, explanation, quiz generation, summarization, and learning recommendations. The document's older Gemini 1.5 Pro/SDK examples are modernized to Google's current `google-genai` SDK and configurable Gemini model.

## Setup

1. Install Python 3.10+ and VS Code.
2. Open this folder in VS Code.
3. Create and activate a virtual environment:

Windows PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

4. Put your Gemini API key in `.env`.
5. Run:
```bash
uvicorn app.main:app --reload
```
6. Open `http://127.0.0.1:8000`.

## Testing
```bash
pytest -q
```
Tests mock Gemini calls, so a live API key is not required for the test suite.

## API
- GET `/api/health`
- POST `/api/qna`
- POST `/api/explain`
- POST `/api/quiz`
- POST `/api/summarize`
- POST `/api/learn/recommendations`

Legacy routes from the supplied document are also supported: `/qna`, `/explain`, `/quiz`, `/summarize`, and `/learn/recommendations?topic=...`.

## Demo mode
Set `DEMO_MODE=true` in `.env` to test the UI without a Gemini key. Demo responses are clearly marked.
