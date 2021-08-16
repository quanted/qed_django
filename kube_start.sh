#!/bin/bash

django-admin collectstatic --noinput --settings=settings_aws_stg       # "Collect" static files (--noinput executes the command w/o user interaction)
django-admin migrate auth --noinput --settings=settings_aws_stg           # used for login
django-admin migrate sessions --noinput --settings=settings_aws_stg       # used for login
exec uwsgi /etc/uwsgi/uwsgi.ini                 # Start uWSGI (HTTP router that binds Python WSGI to a web server, e.g. NGINX)
