FROM python:3.11-slim

# System deps for OpenCV and Tesseract
RUN apt-get update &&     DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends         tesseract-ocr         libtesseract-dev         libgl1         libglib2.0-0         && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Expose default port used by Render (will be ignored if platform sets PORT)
ENV PORT=10000
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
