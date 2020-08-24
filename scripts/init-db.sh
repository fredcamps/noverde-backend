#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    SELECT 'CREATE DATABASE noverde'
           WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'noverde');
    GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_USER TO noverde;
EOSQL
