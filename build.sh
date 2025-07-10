#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

# cd backend  # 👈 Go into the folder containing manage.py

# python manage.py collectstatic --no-input
# python manage.py migrate

#!/bin/bash
pip install -r backend/requirements.txt
python backend/manage.py collectstatic --noinput
