#!/bin/bash

# Wait for MySQL container to be up
until mysql -h mysql -u root -pMolhamhaj90 -e "SELECT 1"; do
    echo "Waiting for MySQL container to be up..."
    sleep 1
done

# Apply database migrations
echo "Apply database migrations"
python manage.py makemigrations
python manage.py migrate


# Start server
echo "Starting server"
python3 manage.py runserver 0.0.0.0:8000

