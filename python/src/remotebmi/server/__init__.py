# Ignore untyped imports: connexion has no type stubs yet;
#   https://github.com/spec-first/connexion/pull/1947
# mypy: disable-error-code="import-untyped,no-any-unimported"

import contextlib
from collections.abc import AsyncIterator
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

from remotebmi.server.build import from_env
from remotebmi.server.compression import ValueCompressionMiddleware


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
    if not openapi_path.is_file():
        # Editable installs and source checkouts use the repository specification.
        openapi_path = Path(__file__).resolve().parents[4] / "openapi.yaml"
    app.add_api(openapi_path, resolver=RelativeResolver("remotebmi.server.api"))
    # Decode requests before validation and compress responses afterward.
    app.add_middleware(
        ValueCompressionMiddleware,
        position=MiddlewarePosition.BEFORE_VALIDATION,
    )
    app.add_error_handler(Exception, handle_model_error)
    return app


def main(**kwargs):  # type: ignore[no-untyped-def]
    model = from_env()
    app = make_app(model)
    port = int(environ.get("BMI_PORT", "50051"))
    uvicorn.run(app, port=port, **kwargs)


if __name__ == "__main__":
    main()
