"""Server capabilities shared by the Python client and server."""

from typing import Literal, TypedDict


class RemotebmiCapabilities(TypedDict):
    """Supported transfer formats and metadata needed to interpret binary values."""

    bmi_version: str
    remotebmi_version: str
    supports_binary: bool
    index_type: str
    byte_order: Literal["little", "big"]
    supports_zstd: bool
