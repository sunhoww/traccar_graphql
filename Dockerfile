FROM python:3.6-alpine

MAINTAINER Sun Howwrongbum <sun@libermatic.com>

WORKDIR /app


COPY ./traccar_graphql /app/traccar_graphql
COPY ./setup.py /app/setup.py
RUN pip install --upgrade pip \
  && pip install -e . \
  && pip install gunicorn

COPY ./config /config

ENV PYTHONPATH /app

EXPOSE 8080
ENTRYPOINT ["/usr/local/bin/gunicorn", "--config", "/config/gunicorn.conf"]
CMD ["traccar_graphql:app"]
