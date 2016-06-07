#!/bin/sh
awk 'BEGIN { cmd="cp -ri /var/www/html/media/* ./media/"; print "n" |cmd; }'
