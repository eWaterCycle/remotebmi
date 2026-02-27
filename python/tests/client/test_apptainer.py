import subprocess
from collections.abc import Generator
from pathlib import Path

import pytest

from remotebmi.client.apptainer import BmiClientApptainer, DeadContainerError

try:
    _apptainer_available = (
        subprocess.run(
            ["apptainer", "--version"],  # noqa: S607
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        ).returncode
        == 0
    )
except OSError:
    _apptainer_available = False

pytestmark = pytest.mark.skipif(
    not _apptainer_available,
    reason="apptainer is unavailable",
)


@pytest.fixture
def leakybucket_def() -> Path:
    return Path(__file__).parent / "fixtures" / "leakybucket.def"


@pytest.fixture
def leakybucket_image(leakybucket_def: Path) -> Path:
    image = leakybucket_def.parent / "leakybucket.sif"
    if image.exists():
        return image
    subprocess.run(["apptainer", "build", str(image), str(leakybucket_def)], check=True)  # noqa: S603, S607
    return image


@pytest.fixture
def leakybucket_client(
    leakybucket_image: Path, tmp_path: Path
) -> Generator[BmiClientApptainer, None, None]:
    client = BmiClientApptainer(
        image=str(leakybucket_image),
        work_dir=str(tmp_path),
    )
    yield client
    del client


def test_get_component_name(leakybucket_client: BmiClientApptainer) -> None:
    assert leakybucket_client.get_component_name() == "leakybucket"


def test_image_not_found(tmp_path: Path) -> None:
    bad_image = tmp_path / "nonexistent_image.sif"
    with pytest.raises(DeadContainerError):
        BmiClientApptainer(image=str(bad_image), work_dir=str(tmp_path))
