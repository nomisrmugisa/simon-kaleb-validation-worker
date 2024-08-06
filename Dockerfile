ARG PYTHON_VERSION=3.11.4
FROM --platform=linux/amd64 python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY Pipfile .
COPY Pipfile.lock .

RUN --mount=type=cache,target=/root/.cache/pip

RUN python -m pip install pipenv
RUN pipenv install --dev --system 

COPY . .

RUN mkdir -p downloads

EXPOSE 8005

CMD fastapi run --host=0.0.0.0 --port=8005