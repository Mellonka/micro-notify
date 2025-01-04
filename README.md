# Уведомления на микросервисах

## Запуск notify-gateway

1. В файле .env  укажите переменные указанные в template.env. Если бд или очередь не созданы, то можно использоваь команды make gateway_pg_start или make rabbit_start.
2. Чтобы накатить миграции нужно выполнить команду alembic revision --autogenerate и alembic upgrade head. Если запускаетс вне докера, то надо изменить NOTIFICATION_POSTGRES_HOST на localhost
3. Чтобы поднять notify-gateway нужно выполнить docker compose up -d gateway outbox.

