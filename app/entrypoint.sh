#!/bin/sh

set -o errexit
set -o nounset

python manage.py migrate
exec "$@"
