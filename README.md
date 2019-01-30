# traccar_graphql

A graphql API for the traccar server

## Environment variables

| Variable               | Description                                                                     |
| ---------------------- | ------------------------------------------------------------------------------- |
| `TRACCAR_BACKEND`      | URI of the **traccar** server. _Required._                                      |
| `JWT_SECRET`           | Secret to sign JWT tokens. Internally set to **flask** `SECRET_KEY` _Required._ |
| `FLASK_ENV`            | Set to `development` to enable various debug features                           |
| `DEVELOPMENT_FRONTEND` | URL of the development server to enable CORS                                    |

## Docker

Service uses `gunicorn`. Pass its command line options by setting environment
variables. For example to pass `--access-logfile file.log` set
`GUNICORN_ACCESSLOG=file.log`.

See http://docs.gunicorn.org/en/latest/settings.html, for available options.
