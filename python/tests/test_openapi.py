from pathlib import Path

import pytest

from remotebmi import openapi


@pytest.mark.parametrize("spec_location", ["openapi.yaml", "../../../openapi.yaml"])
def test_get_openapi_path(
    spec_location: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    module_path = tmp_path / "repo/python/src/remotebmi/openapi.py"
    expected_path = (module_path.parent / spec_location).resolve()
    expected_path.parent.mkdir(parents=True)
    expected_path.touch()
    monkeypatch.setattr(openapi, "__file__", str(module_path))

    actual_path = openapi.get_openapi_path()

    assert actual_path == expected_path
