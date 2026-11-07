# BountyCode backend — production image (Python 3.12 + uvicorn).
FROM python:3.12-slim

# Set untracked PYTHONDONTWRITEBYTECODE/PYTHONUNBUFFERED for clean logs.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps needed by PyMuPDF (PDF text extraction) build/import on slim.
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps first (better layer caching).
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend application package + data assets.
COPY app/ ./app/
COPY scripts/ ./scripts/

# Runtime defaults. Do NOT bake secrets here — pass them via env at run time.
ENV HOST=0.0.0.0 \
    PORT=8000

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request,sys; urllib.request.urlopen('http://127.0.0.1:8000/api/v1/health/live', timeout=5)" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
