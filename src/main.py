import asyncio
import logging
import signal

from typing import AsyncGenerator

import aiohttp

from aiohttp.web import Application, run_app
from src.config import LOGGING_LEVEL
from src.handlers.handlers import routes


logger = logging.getLogger(__name__)
logger.setLevel(LOGGING_LEVEL)


async def http_client_session_ctx(app: Application) -> AsyncGenerator:
    app["session"] = aiohttp.ClientSession()

    yield

    await app["session"].close()


def sig_handler(loop: asyncio.AbstractEventLoop, sig: str) -> None:
    logging.info(f"Receive interrupt signal: {sig}")
    loop.stop()


def main():
    loop = asyncio.get_event_loop()

    loop.add_signal_handler(signal.SIGINT, sig_handler, loop, "SIGINT")
    loop.add_signal_handler(signal.SIGTERM, sig_handler, loop, "SIGTERM")

    app = Application()
    app.cleanup_ctx.append(http_client_session_ctx)

    app.add_routes(routes)

    try:
        run_app(app, host="0.0.0.0", port=8080)
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt")
    finally:
        loop.stop()
    loop.close()

    logger.info("Shutdown :(")


if __name__ == "__main__":
    main()
