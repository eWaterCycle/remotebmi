"""Locate the shared OpenAPI specification."""

from pathlib import Path


def get_openapi_path() -> Path:
    """Return the path to the shared OpenAPI specification.

    Prefer the bundled specification, falling back to the repository copy for
    editable installs and source checkouts.

    Returns:
        Path to the OpenAPI YAML file.
    """
    openapi_path = Path(__file__).parent / "openapi.yaml"
    if not openapi_path.is_file():
        # Editable installs and source checkouts use the repository specification.
        openapi_path = Path(__file__).resolve().parents[3] / "openapi.yaml"
    return openapi_path
