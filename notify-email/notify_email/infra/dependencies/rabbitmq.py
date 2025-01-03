from aio_pika import connect_robust
from aio_pika.robust_channel import RobustChannel

from dependency_injector import containers, providers


class RabbitMQContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    connection = providers.Resource(
        connect_robust,
        login=config.rabbitmq.user,
        password=config.rabbitmq.password,
        host=config.rabbitmq.host,
        port=config.rabbitmq.port,
    )
    channel = providers.Resource(
        RobustChannel,
        connection=connection,
    )


async def get_container() -> RabbitMQContainer:
    container = RabbitMQContainer()

    container.config.rabbitmq.user.from_env("RABBITMQ_USER", required=True)
    container.config.rabbitmq.password.from_env("RABBITMQ_PASSWORD", required=True)
    container.config.rabbitmq.host.from_env("RABBITMQ_HOST", required=True)
    container.config.rabbitmq.port.from_env("RABBITMQ_PORT", required=True, as_=int)

    return container
