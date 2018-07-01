FROM python:2.7-alpine

MAINTAINER Sun Howwrongbum <sun@libermatic.com>

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt && pip install gunicorn

COPY ./traccar_graphql /app/traccar_graphql
COPY ./gunicorn.conf /gunicorn.conf

ENV PYTHONPATH /app

EXPOSE 8080
ENTRYPOINT ["/usr/local/bin/gunicorn", "--config", "/gunicorn.conf", "traccar_graphql:app"]
