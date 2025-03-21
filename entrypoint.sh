#!/bin/sh

# Wait for the database to be ready
while ! pg_isready -h db -p 5432 -U username; do
  echo "Waiting for the database to be ready..."
  sleep 2
done

# Run database migrations
flask db upgrade

# Start the Flask application
flask run --host=0.0.0.0
