import logging.config

from dependency_injector import containers, providers


class LoggingContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    logging = providers.Resource(logging.config.dictConfig, config.logging)
