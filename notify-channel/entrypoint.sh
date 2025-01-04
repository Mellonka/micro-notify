#!/bin/ash

ls -la
export
alembic upgrade head

echo 'start consume'
sleep 5

python3 notify_channel/infra/scripts/email_consume.py
