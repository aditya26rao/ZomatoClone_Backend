set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-inputpy 

python manage.py migrate

