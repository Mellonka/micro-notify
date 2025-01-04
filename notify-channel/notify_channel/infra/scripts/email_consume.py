import asyncio

from notify_channel.infra.dependencies.application import get_app_container


async def main() -> None:
    app_cont = get_app_container()
    await app_cont.init_resources()  # type: ignore
    consumer = await app_cont.email_queue_consumer.async_()
    await consumer.run()


if __name__ == "__main__":
    asyncio.run(main())
