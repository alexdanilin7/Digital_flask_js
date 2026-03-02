FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .


RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt
FROM python:3.11-slim

RUN useradd -m -u 1000 appuser

COPY --from=builder /opt/venv /opt/venv

WORKDIR /app
COPY --chown=appuser:appuser . .

ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

USER appuser

EXPOSE 5001

CMD ["python", "app.py"]