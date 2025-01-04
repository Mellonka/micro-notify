from dependency_injector import containers, providers


class ConfigContainer(containers.DeclarativeContainer):
    config = providers.Configuration(
        yaml_files=["notify_channel/infra/configs/main.yaml"]
    )
