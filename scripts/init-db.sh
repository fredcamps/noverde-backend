#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE noverde;
    GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_USER TO noverde;
EOSQL
