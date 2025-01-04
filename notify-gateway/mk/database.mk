# RabbitMQ

rabbitmq_start: rabbitmq_down create_network
	docker run \
	--name $(RABBITMQ_CONTAINER_NAME) \
	--hostname $(RABBITMQ_CONTAINER_NAME) \
	--volume $(RABBITMQ_VOLUME):/var/lib/rabbitmq \
	--network $(DOCKER_NETWORK) \
	-p $(RABBITMQ_PORT):5672 \
	-p $(RABBITMQ_MANAGEMENT_PORT):15672 \
	-e RABBITMQ_DEFAULT_USER=$(RABBITMQ_USER) \
	-e RABBITMQ_DEFAULT_PASS=$(RABBITMQ_PASSWORD) \
	-d rabbitmq:4.0.5-management-alpine

rabbitmq_down:
	docker rm --force $(RABBITMQ_CONTAINER_NAME)

rabbitmq_clean:
	docker volume rm $(RABBITMQ_VOLUME)

rabbitmq_stop:
	docker stop $(RABBITMQ_CONTAINER_NAME)

rabbitmq_bash:
	docker exec -it $(RABBITMQ_CONTAINER_NAME) bash


# PostgreSQL

postgres_sql:
	docker exec -it $(POSTGRES_CONTAINER_NAME) psql -U $(POSTGRES_USER)

postgres_start: postgres_down create_network
	docker run \
	--name $(POSTGRES_CONTAINER_NAME) \
	--volume $(POSTGRES_VOLUME):/var/lib/postgresql/data \
	--network $(DOCKER_NETWORK) \
	-p $(POSTGRES_PORT):5432 \
	--env-file .env \
	-d postgres:17.2-alpine

postgres_down:
	docker rm --force $(POSTGRES_CONTAINER_NAME)

postgres_clean:
	docker volume rm $(POSTGRES_VOLUME)

postgres_stop:
	docker stop $(POSTGRES_CONTAINER_NAME)

postgres_bash:
	docker exec -it $(POSTGRES_CONTAINER_NAME) bash


# General

database_down: postgres_down rabbitmq_down

database_clean: postgres_clean rabbitmq_clean

database_start: postgres_start rabbitmq_start

database_stop: postgres_stop rabbitmq_stop
