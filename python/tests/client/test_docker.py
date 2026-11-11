# mypy: disable-error-code="no-untyped-def"

from contextlib import closing
from types import SimpleNamespace

import pytest

from remotebmi.client.docker import BmiClientDocker


class FakeContainer:
    status = "running"

    def reload(self):
        pass

    def stop(self):
        pass


@pytest.mark.parametrize("mode", [None, True, False])
def test_docker_forwards_compression(mode, tmp_path, monkeypatch):
    def run_container(*args, **kwargs):
        return FakeContainer()

    docker_client = SimpleNamespace(containers=SimpleNamespace(run=run_container))
    monkeypatch.setattr(
        "remotebmi.client.docker.docker.from_env", lambda: docker_client
    )
    kwargs = {} if mode is None else {"compression": mode}
    client = BmiClientDocker(
        "model", str(tmp_path), host="localhost", delay=0, **kwargs
    )
    with closing(client.client):
        assert client.compression is (mode or False)
