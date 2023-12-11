#! /usr/bin/env sh
# prestart.sh

set -e

# Let the DB start and wait until it is running
until PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -d "$POSTGRES_DB" -U "$POSTGRES_USER" -c '\q'; do

  >&2 echo "Postgres is not available yet - sleeping while waiting for it to start"
  sleep 1
done

>&2 echo "Postgres is up - running the application"

# Run table creations
PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -d "$POSTGRES_DB" -U "$POSTGRES_USER" -f ./src/database/schemas.sql

# Ingest initial data to the database.
python ./src/database/ingest_bootstrap.py