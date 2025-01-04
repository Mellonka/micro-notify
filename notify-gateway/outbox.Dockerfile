FROM python:3.12-alpine as requirements-stage

WORKDIR /temp

RUN pip install poetry

COPY pyproject.toml poetry.lock* /temp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY --from=requirements-stage /temp/requirements.txt /requirements.txt

RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY src /code/src
COPY src/outbox.py /code/
COPY .env /code/.env

WORKDIR /code

RUN ls -la
CMD python3 outbox.py