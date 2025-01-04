import aiosmtplib
from dependency_injector import containers, providers



async def _smtp(*args, **kwargs):
    async with aiosmtplib.SMTP(*args, **kwargs) as smtp:
        yield smtp


class SMTPContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    smtp = providers.Resource(
        _smtp,
        hostname=config.smtp.hostname,
        port=config.smtp.port,
        username=config.smtp.username,
        password=config.smtp.password,
        use_tls=config.smtp.use_tls,
    )

    @classmethod
    def set_config_from_env(cls, config: providers.Configuration):
        config.smtp.username.from_env("SMTP_USER", required=True)
        config.smtp.hostname.from_env("SMTP_HOST", required=True)
        config.smtp.password.from_env("SMTP_PASSWORD", required=True)
        config.smtp.port.from_env("SMTP_PORT", required=True, as_=int)
