# mypy: disable-error-code="no-untyped-def"

import pytest
from jsonschema import ValidationError

from remotebmi.capabilities import RemotebmiCapabilities, parse_capabilities

CAPABILITIES = RemotebmiCapabilities(
    bmi_version="2.0",
    remotebmi_version="0.1.1",
    supports_binary=False,
    index_type="int64",
    byte_order="little",
    supports_zstd=True,
)


@pytest.mark.parametrize("body", [None, [], "invalid", 1, True])
def test_capabilities_rejects_non_object(body):
    with pytest.raises(ValidationError):
        parse_capabilities(body)


@pytest.mark.parametrize("field", list(CAPABILITIES))
def test_capabilities_rejects_missing_field(field):
    body = dict(CAPABILITIES)
    del body[field]

    with pytest.raises(ValidationError):
        parse_capabilities(body)


@pytest.mark.parametrize(
    "field, value",
    [
        ("bmi_version", 2),
        ("remotebmi_version", None),
        ("supports_binary", 1),
        ("supports_binary", "false"),
        ("index_type", "int16"),
        ("index_type", 64),
        ("byte_order", "middle"),
        ("byte_order", []),
        ("supports_zstd", 1),
        ("supports_zstd", "true"),
    ],
)
def test_capabilities_rejects_invalid_field(field, value):
    body = {**CAPABILITIES, field: value}

    with pytest.raises(ValidationError):
        parse_capabilities(body)


def test_capabilities_rejects_unknown_field():
    body = {**CAPABILITIES, "unexpected": True}

    with pytest.raises(ValidationError, match="Additional properties"):
        parse_capabilities(body)
