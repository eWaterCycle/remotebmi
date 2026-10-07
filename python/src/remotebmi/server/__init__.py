# Ignore untyped imports: connexion has no type stubs yet;
#   https://github.com/spec-first/connexion/pull/1947
# mypy: disable-error-code="import-untyped,no-any-unimported"

import contextlib
import logging
from collections.abc import AsyncIterator
from os import environ
from pathlib import Path
from traceback import format_exception

import uvicorn
from bmipy import Bmi
from connexion import AsyncApp, ConnexionMiddleware, problem
from connexion.lifecycle import ConnexionRequest, ConnexionResponse
from connexion.options import SwaggerUIOptions
from connexion.resolver import RelativeResolver

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


def make_app(model: Bmi) -> AsyncApp:
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
    return app


def main(**kwargs):  # type: ignore[no-untyped-def]
    model = from_env()
    app = make_app(model)
    port = int(environ.get("BMI_PORT", "50051"))
    uvicorn.run(app, port=port, **kwargs)


if __name__ == "__main__":
    main()
