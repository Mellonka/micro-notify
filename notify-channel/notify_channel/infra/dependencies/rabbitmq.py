from aio_pika import connect_robust
from aio_pika.abc import AbstractRobustConnection, AbstractChannel
from aio_pika.robust_channel import RobustChannel

from dependency_injector import containers, providers


async def _connection(*args, **kwargs):
    connection = await connect_robust(*args, **kwargs)
    async with connection:
        yield connection
    await connection.close()


async def _channel(connection: AbstractRobustConnection):
    async with RobustChannel(connection) as channel:
        yield channel


async def declare_queue(channel: AbstractChannel, *args, **kwargs):
    yield await channel.declare_queue(*args, **kwargs)


class RabbitMQContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    connection = providers.Resource(
        _connection,
        login=config.rabbitmq.user,
        password=config.rabbitmq.password,
        host=config.rabbitmq.host,
        port=config.rabbitmq.port,
    )
    channel = providers.Resource(_channel, connection)
    # declare_queue = providers.Callable(_declare_queue)  # TODO разобраться как функцию тоже сделать зависимостью

    @classmethod
    def set_config_from_env(cls, config: providers.Configuration):
        config.rabbitmq.user.from_env("RABBITMQ_USER", required=True)
        config.rabbitmq.password.from_env("RABBITMQ_PASSWORD", required=True)
        config.rabbitmq.host.from_env("RABBITMQ_HOST", required=True)
        config.rabbitmq.port.from_env("RABBITMQ_PORT", required=True, as_=int)
