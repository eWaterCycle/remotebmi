import contextlib
from os import environ
from typing import AsyncIterator

from bmipy import Bmi
from connexion import AsyncApp, ConnexionMiddleware
from connexion.resolver import RelativeResolver
from connexion.options import SwaggerUIOptions

from remotebmi.server.build import from_env

def make_app(model: Bmi):
    @contextlib.asynccontextmanager
    async def lifespan_handler(app: ConnexionMiddleware) -> AsyncIterator:
        yield {"model": model}

    app = AsyncApp(
        "remotebmi.server",
        strict_validation=True,
        swagger_ui_options=SwaggerUIOptions(swagger_ui=False),
        lifespan=lifespan_handler,
    )

    app.add_api("openapi.yaml", resolver=RelativeResolver("remotebmi.server.api"))
    return app

def main(**kwargs):
    model = from_env()
    app = make_app(model)
    port = int(environ.get('BMI_PORT', 50051))
    app.run(port=port, **kwargs)

if __name__ == "__main__":
    main()
