from functools import partial

import aioredis
import sentry_sdk
import uvicorn
from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from config import set_logging_config, settings
from endpoints import router


async def startup(app):
    redis = aioredis.from_url(settings.redis_dsn)
    app.state.redis_pool = redis


async def shutdown(app):
    await app.state.redis.redis_pool.disconnect()


def get_app():
    set_logging_config()

    app = FastAPI(
        title="Tickets API",
        debug=settings.debug,
    )

    if settings.sentry_dsn:
        sentry_sdk.init(
            dsn=settings.sentry_dsn,
        )
        app.add_middleware(SentryAsgiMiddleware)

    app.include_router(router)

    app.add_event_handler(event_type="startup", func=partial(startup, app=app))
    app.add_event_handler(event_type="shutdown", func=partial(shutdown, app=app))
    return app


if __name__ == "__main__":
    uvicorn.run(
        "main:get_app",
        workers=settings.workers,
        factory=True,
        host=settings.listen_addr,
        port=settings.listen_port,
        reload=settings.debug,
        log_level="debug" if settings.debug else "info",
    )
