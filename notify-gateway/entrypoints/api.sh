#!/bin/ash

ls -la
export

echo 'start consume'
sleep 5

alembic upgrade head
uvicorn src.main:app --host 0.0.0.0 --port 10000
