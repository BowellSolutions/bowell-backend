"""
Description: Package contains settings:
- base      # base settings such as debug, allowed_hosts, installed_apps, middlewares, url conf, templates, wsgi, asgi
            # applications, dev and CI database setup, validators, static and media paths, installed packages configs

- dev       # extends base with dev database, channel_layers, redis broker, model mock

- heroku    # extends prod with redis and postgres setup for prod, celery

- prod      # extends base with allowed_hosts, cors, static and media in prod - whitenoise, redis and postgres,
            # channel_layers setup
"""
