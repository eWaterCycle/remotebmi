# Ignore untyped imports: connexion has no type stubs yet;
#   https://github.com/spec-first/connexion/pull/1947
# mypy: disable-error-code="import-untyped,no-any-unimported"

import contextlib
import logging
from collections.abc import AsyncIterator, Sequence
from os import environ
from pathlib import Path
from traceback import format_exception

import uvicorn
from bmipy import Bmi
from connexion import AsyncApp, ConnexionMiddleware, problem
from connexion.lifecycle import ConnexionRequest, ConnexionResponse
from connexion.middleware import MiddlewarePosition
from connexion.options import SwaggerUIOptions
from connexion.resolver import RelativeResolver
from starlette.middleware.cors import CORSMiddleware

from remotebmi._http import CORS_MAX_AGE, CORS_METHODS
from remotebmi.server.build import from_env


class _MultipleContentTypesFilter(logging.Filter):
    """Drop connexion warning logged on each request to set_value.

    The warning is about the operation accepting JSON and octet-stream,
    but connexion does use the content type of the request.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        return not record.getMessage().startswith(
            "this operation accepts multiple content types"
        )


logging.getLogger("connexion.operations.openapi3").addFilter(
    _MultipleContentTypesFilter()
)


def handle_model_error(request: ConnexionRequest, exc: Exception) -> ConnexionResponse:  # noqa: ARG001
    exc_class = str(exc.__class__.__name__)
    ext = {"traceback": format_exception(exc)}
    return problem(
        500, type=exc_class, title="Model raised " + exc_class, detail=str(exc), ext=ext
    )


def cors_origins_from_env() -> list[str] | None:
    """Origins allowed to call the server from a browser.

    Read from BMI_CORS_ORIGINS environment variable,
    a comma separated list of origins or `*` for any origin.
    """
    value = environ.get("BMI_CORS_ORIGINS", "")
    return [origin.strip() for origin in value.split(",") if origin.strip()] or None


def make_app(model: Bmi, cors_origins: Sequence[str] | None = None) -> AsyncApp:
    """Make ASGI app that serves the model using connexion and openapi.yaml.

    Args:
        model: The model to serve.
        cors_origins: Origins allowed to call the server from a browser,
            `["*"]` for any origin. Default is no CORS headers.
    """

    @contextlib.asynccontextmanager
    async def lifespan_handler(app: ConnexionMiddleware) -> AsyncIterator:  # noqa: ARG001
        yield {"model": model}

    app = AsyncApp(
        "remotebmi.server",
        strict_validation=True,
        swagger_ui_options=SwaggerUIOptions(swagger_ui=False),
        lifespan=lifespan_handler,
    )

    openapi_path = Path(__file__).parent / "openapi.yaml"
    app.add_api(openapi_path, resolver=RelativeResolver("remotebmi.server.api"))
    app.add_error_handler(Exception, handle_model_error)
    if cors_origins:
        app.add_middleware(
            CORSMiddleware,
            position=MiddlewarePosition.BEFORE_EXCEPTION,
            allow_origins=cors_origins,
            allow_methods=CORS_METHODS,
            allow_headers=["*"],
            max_age=CORS_MAX_AGE,
        )
    return app


def main(**kwargs):  # type: ignore[no-untyped-def]
    model = from_env()
    app = make_app(model, cors_origins=cors_origins_from_env())
    port = int(environ.get("BMI_PORT", "50051"))
    uvicorn.run(app, port=port, **kwargs)


if __name__ == "__main__":
    main()
