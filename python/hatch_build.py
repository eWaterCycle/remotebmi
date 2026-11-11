from pathlib import Path
from typing import Any

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
    """Bundle the repository's OpenAPI specification in Python distributions."""

    def initialize(self, version: str, build_data: dict[str, Any]) -> None:  # noqa: ARG002
        spec = Path(self.root).parent / "openapi.yaml"
        if spec.is_file():
            destination = Path("remotebmi/openapi.yaml")
            if self.target_name == "sdist":
                destination = Path("src") / destination
            build_data["force_include"][str(spec)] = destination.as_posix()
