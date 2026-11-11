"""Server capabilities shared by the Python client and server."""

from typing import Any, Literal, TypedDict

import yaml
from jsonschema import Draft4Validator

from remotebmi.openapi import get_openapi_path


class RemotebmiCapabilities(TypedDict):
    """Supported transfer formats and metadata needed to interpret binary values."""

    bmi_version: str
    remotebmi_version: str
    supports_binary: bool
    index_type: str
    byte_order: Literal["little", "big"]
    supports_zstd: bool


def capabilities_validator() -> Draft4Validator:
    """Load the shared OpenAPI capabilities schema."""
    with get_openapi_path().open() as spec:
        schema = yaml.safe_load(spec)["components"]["schemas"]["RemotebmiCapabilities"]
    return Draft4Validator(schema)


def parse_capabilities(data: Any) -> RemotebmiCapabilities:
    """Validate server JSON and construct the capabilities dictionary."""
    capabilities_validator().validate(data)
    return RemotebmiCapabilities(
        bmi_version=data.get("bmi_version"),
        remotebmi_version=data.get("remotebmi_version"),
        supports_binary=data.get("supports_binary"),
        index_type=data.get("index_type"),
        byte_order=data.get("byte_order"),
        supports_zstd=data.get("supports_zstd"),
    )
