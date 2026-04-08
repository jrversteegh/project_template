import os
from pathlib import Path
import logging

import pytest

_script_dir = Path(os.path.dirname(os.path.realpath(__file__)))
_output_dir = _script_dir / "output"
_data_dir = _script_dir / "data"
_log_dir = _script_dir / "logs"

os.chdir(_script_dir)

def pytest_configure(config):
    if "PYTEST_XDIST_WORKER" in os.environ:
        worker_id = "_" + os.environ["PYTEST_XDIST_WORKER"]
    else:
        worker_id = datetime.now().strftime("%Y%m%d%H%M%S")
        _logname = _log_dir / f"pytest{worker_id}.log"
        log_link = _log_dir / "test.log"
        if log_link.exists():
            os.remove(log_link)
            os.symlink(_logname, log_link)

    logging.basicConfig(
        filename=str(_logname),
        level=logging.DEBUG,
        filemode="w",
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

@pytest.fixture
def data_dir():
    return _data_dir


@pytest.fixture
def output_dir():
    return _output_dir
