FROM python:3.12.7

ARG ENVIRONMENT
ENV ENVIRONMENT ${ENVIRONMENT}
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    git \
    tini \
    && apt-get clean

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app
RUN git config --global --add safe.directory /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root $(test "ENVIRONMENT" = production && echo "--only main") --no-interaction

COPY . .