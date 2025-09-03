# build stage to install dependencies
FROM python:3.11-slim AS builder

WORKDIR /app

# prevent pyc files, enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# final stage, just copy things we need
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY ./src ./src

ENV PATH="/opt/venv/bin:$PATH"

# start the server
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
