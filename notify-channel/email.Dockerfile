FROM python:3.12-alpine as requirements-stage

WORKDIR /temp

RUN pip install poetry

COPY pyproject.toml poetry.lock* /temp/
COPY notify-shared /temp/notify-shared

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY --from=requirements-stage /temp/requirements.txt /requirements.txt
COPY --from=requirements-stage /temp/notify-shared /temp/notify-shared

RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY notify_channel /code/notify_channel
COPY migrations /code/migrations
COPY .env /code
COPY log /code/log
COPY alembic.ini /code
COPY entrypoint.sh /code

WORKDIR /code

ENV PYTHONPATH=/code:

RUN chmod a+x /code/entrypoint.sh

ENTRYPOINT [ "/code/entrypoint.sh" ]
