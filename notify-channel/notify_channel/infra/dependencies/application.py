import dotenv
from dependency_injector import containers, providers

from notify_channel.application.commands.send_email import SendEmailHandler
from notify_channel.infra.dependencies.config import ConfigContainer
from notify_channel.infra.dependencies.logging import LoggingContainer
from notify_channel.infra.dependencies.rabbitmq import RabbitMQContainer, declare_queue
from notify_channel.infra.dependencies.smtp import SMTPContainer
from notify_channel.infra.dependencies.sqlalchemy import SQLAlchemyContainer
from notify_channel.infra.email.queue.consumer import RabbitMQConsumer
from notify_channel.infra.email.queue.producer import RabbitMQProducer
from notify_channel.infra.email.service import EmailService


class ApplicationContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    logging_cont = providers.Container(LoggingContainer, config=config)
    smtp_cont = providers.Container(SMTPContainer, config=config)
    rabbitmq_cont = providers.Container(RabbitMQContainer, config=config)
    sqlalchemy_cont = providers.Container(SQLAlchemyContainer, config=config)

    email_event_queue = providers.Resource(
        declare_queue,
        channel=rabbitmq_cont.channel,
        name=config.email.queue.events,
        durable=True,
    )
    email_event_queue_producer = providers.Factory(
        RabbitMQProducer,
        queue=email_event_queue,
    )
    email_service = providers.Singleton(
        EmailService,
        smtp=smtp_cont.smtp,
        smtp_username=config.smtp.username,
        event_producer=email_event_queue_producer,
    )

    email_queue = providers.Resource(
        declare_queue,
        channel=rabbitmq_cont.channel,
        name=config.email.queue.notify,
        durable=True,
    )
    send_email_handler = providers.Factory(
        SendEmailHandler,
        email_service=email_service,
        unit_of_work=sqlalchemy_cont.unit_of_work,
    )
    email_queue_consumer = providers.Factory(
        RabbitMQConsumer,
        queue=email_queue,
        handler=send_email_handler,
    )


def get_app_container() -> ApplicationContainer:
    dotenv.load_dotenv()

    config_cont = ConfigContainer()
    RabbitMQContainer.set_config_from_env(config_cont.config)
    SMTPContainer.set_config_from_env(config_cont.config)
    SQLAlchemyContainer.set_config_from_env(config_cont.config)
    return ApplicationContainer(config=config_cont.config)
