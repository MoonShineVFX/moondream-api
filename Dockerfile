FROM python:3.7-slim

ENV PYTHONUNBUFFERED TRUE
ENV PORT 80

WORKDIR /app

RUN pip install gunicorn

RUN pip install pipenv --no-cache-dir
RUN apt-get update && apt-get install -y --no-install-recommends gcc
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --system --deploy --ignore-pipfile

COPY . ./

CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 app:app
