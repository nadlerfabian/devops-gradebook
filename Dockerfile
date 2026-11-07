FROM python:3.12-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN python -m venv /opt/venv \
    && /opt/venv/bin/python -m pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim AS runtime

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN groupadd --system gradebook \
    && useradd --system --gid gradebook gradebook
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY app ./app
COPY wsgi.py .

USER gradebook
EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=3s --start-period=15s --retries=3 \
    CMD ["python", "-c", "from urllib.request import urlopen; urlopen('http://127.0.0.1:8000/health', timeout=2).close()"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "--access-logfile", "-", "wsgi:app"]
