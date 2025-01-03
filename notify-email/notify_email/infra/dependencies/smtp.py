import aiosmtplib
from dependency_injector import containers, providers
from aio_pika.robust_queue import RobustQueue

from notify_email.application.commands.send_email import (
    SendEmailHandler,
)
from notify_email.infra.email.services.smtp import SmtpEmailService
from notify_email.infra.dependencies.sqlalchemy import SQLAlchemyContainer
from notify_email.infra.email.queue.consumer import RabbitMQConsumer


class ServiceContainer(containers.DeclarativeContainer):
    config = providers.Configuration(
        yaml_files=["notify_email/infra/configs/main.yaml"]
    )

    rabbitmq_cont = providers.DependenciesContainer()
    logging_cont = providers.DependenciesContainer()

    smtp = providers.Resource(
        aiosmtplib.SMTP,
        hostname=config.from_env("SMTP_HOST"),
        port=config.from_env("SMTP_PORT", as_=int),
        username=config.from_env("SMTP_USERNAME"),
        password=config.from_env("SMTP_PASSWORD"),
        use_tls=config.from_env("SMTP_USE_TLS"),
    )
    smtp_email_service = providers.Singleton(
        SmtpEmailService,
        smtp=smtp,
        username=config.from_env("SMTP_USERNAME"),
    )
    send_email_handler = providers.Factory(
        SendEmailHandler,
        email_service=smtp_email_service,
        unit_of_work=SQLAlchemyContainer.unit_of_work,
    )
    email_queue = providers.Resource(
        RobustQueue,
        channel=rabbitmq_cont.channel,
        name=config.email.queue.notify,
        durable=True,
    )
    email_queue_consumer = providers.Factory(
        RabbitMQConsumer,
        queue=email_queue,
        handler=send_email_handler,
        logger=logging_cont.app_logger,
    )
