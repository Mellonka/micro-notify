#!/bin/ash

ls -la
export

echo 'start consume'
sleep 5

alembic upgrade head

python3 outbox.py
