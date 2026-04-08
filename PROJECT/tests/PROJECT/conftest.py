import logging
import os
from datetime import datetime
from pathlib import Path

import pytest

_script_dir = Path(os.path.dirname(os.path.realpath(__file__)))
_test_dir = _script_dir.parent
_output_dir = _test_dir / "output"
_data_dir = _test_dir / "data"
_log_dir = _test_dir / "logs"

os.makedirs(_output_dir, exist_ok=True)
os.makedirs(_log_dir, exist_ok=True)

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
