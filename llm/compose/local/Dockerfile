FROM docker.io/python:3.12.10-slim-bookworm AS python

# Python build stage
FROM python AS python-build-stage

ARG BUILD_ENVIRONMENT=local

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /app

COPY requirements/local.txt /requirements/local.txt
COPY requirements/base.txt /requirements/base.txt
RUN pip install -r /requirements/local.txt

COPY . .

CMD ["uvicorn", "llm.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 