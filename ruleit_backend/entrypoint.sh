#!/bin/bash

# Wait for the database to be ready
while !</dev/tcp/ruleit_db/5432; do
  sleep 0.5
done

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser if it doesn't already exist
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='${DJANGO_SUPERUSER_USERNAME}').exists():
    User.objects.create_superuser('${DJANGO_SUPERUSER_USERNAME}', '${DJANGO_SUPERUSER_EMAIL}', '${DJANGO_SUPERUSER_PASSWORD}');
"

# Start the Django server
exec python manage.py runserver 0.0.0.0:8000

