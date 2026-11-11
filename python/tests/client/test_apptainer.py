# mypy: disable-error-code="no-untyped-def"

from contextlib import closing

import pytest

from remotebmi.client.apptainer import BmiClientApptainer


class FakeProcess:
    def poll(self):
        return None

    def terminate(self):
        pass

    def wait(self):
        return 0


@pytest.mark.parametrize("mode", [None, True, False])
def test_apptainer_forwards_compression(mode, tmp_path, monkeypatch):
    def start_process(*args, **kwargs):
        return FakeProcess()

    monkeypatch.setattr("remotebmi.client.apptainer.subprocess.Popen", start_process)
    kwargs = {} if mode is None else {"compression": mode}
    client = BmiClientApptainer("model", str(tmp_path), capture_logs=False, **kwargs)
    with closing(client.client):
        assert client.compression is (mode or False)
