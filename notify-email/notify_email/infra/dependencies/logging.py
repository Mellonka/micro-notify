import logging.config

from dependency_injector import containers, providers


class LoggingContainer(containers.DeclarativeContainer):
    config = providers.Configuration(
        yaml_files=["notify_email/infra/configs/logging.yaml"]
    )
    logging = providers.Resource(logging.config.dictConfig, config)
