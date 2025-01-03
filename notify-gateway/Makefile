include .env


gateway_pg_start: app_network
	docker run \
	--name $(NOTIFICATION_POSTGRES_CONTAINER_NAME) \
	--volume $(NOTIFICATION_POSTGRES_VOLUME):/var/lib/postgresql/data \
	--network $(DOCKER_NETWORK) \
	-p $(NOTIFICATION_POSTGRES_PORT):5432 \
	-e POSTGRES_USER=$(NOTIFICATION_POSTGRES_USER) \
	-e POSTGRES_PASSWORD=$(NOTIFICATION_POSTGRES_PASSWORD) \
	-e POSTGRES_DB=$(NOTIFICATION_POSTGRES_DB) \
	-d postgres:16.0-alpine3.18

gateway_pg_down: notification_postgres_stop
	docker rm $(NOTIFICATION_POSTGRES_CONTAINER_NAME)

gateway_pg_stop:
	docker stop $(NOTIFICATION_POSTGRES_CONTAINER_NAME)
	
gateway_pg_exec:
	docker exec -it $(NOTIFICATION_POSTGRES_CONTAINER_NAME) psql -U $(NOTIFICATION_POSTGRES_USER) $(NOTIFICATION_POSTGRES_DB)


rabbit_start: app_network
	docker run \
	--name $(RABBITMQ_CONTAINER_NAME) \
	--hostname $(RABBITMQ_CONTAINER_NAME) \
	--volume $(RABBITMQ_VOLUME):/var/lib/rabbitmq \
	--network $(DOCKER_NETWORK) \
	-p $(RABBITMQ_PORT):5672 \
	-p $(RABBITMQ_MANAGEMENT_PORT):15672 \
	-e RABBITMQ_DEFAULT_USER=$(RABBITMQ_USER) \
	-e RABBITMQ_DEFAULT_PASS=$(RABBITMQ_PASSWORD) \
	-d rabbitmq:3.13.6-management-alpine

rabbit_down: rabbit_stop
	docker rm $(RABBITMQ_CONTAINER_NAME)

rabbit_stop:
	docker stop $(RABBITMQ_CONTAINER_NAME)


app_network:
	-docker network create --attachable $(DOCKER_NETWORK)