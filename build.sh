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