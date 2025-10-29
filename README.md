# spam-detector-web

Flask-based Spam Detector with OCR (image-to-text) support. Ready for deployment on **Render** (Docker) or any container host.

## What’s inside
- `app.py` — Flask app entry (serves `index1.html` at `/`)
- `templates/` & `static/` — UI assets
- `pipeline.py` — spam detection pipeline
- `ocr.py` — OCR helper (uses Tesseract via `pytesseract`)
- `saved-models/` — pre-trained `.pkl` models and vectorizers
- `requirements.txt` — Python deps (includes `opencv-python`, `pytesseract`, `gunicorn`)
- `Dockerfile` — installs system deps (`tesseract-ocr`, `libtesseract-dev`, `libgl1`) and runs `gunicorn`
- `Procfile` — alternative non-Docker run command for platforms that support it

## Local run (no Docker)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# You need Tesseract installed locally:
#   macOS (brew): brew install tesseract
#   Ubuntu: sudo apt-get update && sudo apt-get install -y tesseract-ocr libtesseract-dev
python app.py  # for quick smoke test (Flask dev server if you add a main guard), or:
gunicorn app:app  # recommended
```

## Deploy on Render (Docker)
1. Push this folder to GitHub (e.g. `advait-t/spam-detector-web`).
2. In Render dashboard: **New → Web Service → Build from a Dockerfile**.
3. Point to this repo. No Build/Start commands needed (Dockerfile handles it).
4. Set environment:
   - **PORT**: `10000` (optional; Render will set PORT and gunicorn will respect our CMD; platform may override)
5. Deploy. The app serves `/` → `templates/index1.html`.
6. OCR endpoint is available at `/ocr` and expects an image file via form-data field name `file` (match your UI).

## Deploy on Render (non-Docker)
If you prefer not to use Docker, add Render settings:
- **Environment**: Python 3.11
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

You must also add a Render **apt** build step to install `tesseract-ocr`. This is easiest with Docker, so the Docker route above is recommended.

## Endpoints (from existing code)
- `GET /` — homepage (`index1.html`)
- `POST /predict` — JSON/Text spam prediction
- `POST /ocr` — returns extracted text as JSON

> Note: These routes come from `server.py` original logic now moved to `app.py`. If you add new endpoints, define them in `app.py`.
