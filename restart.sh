#!/bin/sh
killall -9 uwsgi
uwsgi -x wsgi.xml
