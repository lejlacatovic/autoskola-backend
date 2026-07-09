#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py shell -c "
from accounts.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(username='admin', email='lejla.catovic18@gmail.com', password='Admin1234!', role='admin')
    print('Superuser kreiran!')
else:
    print('Vec postoji.')
"

python manage.py shell -c "
from accounts.models import User
if not User.objects.filter(username='admin1').exists():
    User.objects.create_superuser(username='admin1', email='lejla.catovic18@gmail.com', password='Admin1234!!', role='admin')
    print('Novi superuser kreiran!')
else:
    print('Novi superuser vec postoji.')
"