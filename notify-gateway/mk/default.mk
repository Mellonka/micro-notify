RABBITMQ_CONTAINER_NAME=notify-email-rabbitmq
RABBITMQ_VOLUME=notify-email-rabbitmq-data

POSTGRES_CONTAINER_NAME=notify-gateway-postgres
POSTGRES_VOLUME=notify-gateway-postgres-data

DOCKER_NETWORK=micro-notify-network

create_network:
	-docker network create --attachable $(DOCKER_NETWORK)
