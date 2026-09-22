FROM python:3.12-slim

# Least privilege: untrusted code never runs as root.
RUN groupadd -r runner && useradd -r -g runner runner \
    && apt-get update && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /srv && chown runner:runner /srv

WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .

USER runner
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
