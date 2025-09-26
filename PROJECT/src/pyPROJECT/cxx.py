"""
PROJECT C++ module loader

Import object from the PROJECT C++ module
"""

__author__ = "AUTHOR"
__contact__ = "EMAIL"

import importlib
import logging

_log = logging.getLogger("pyPROJECT.cxx")
_module_name = ".pycxxPROJECT"

try:
    _log.info(f"Importing {_module_name}")
    pycxxPROJECT = importlib.import_module(_module_name, package="pyPROJECT")
except ImportError:
    _log.error(f"Failed to import {_module_name}")
    raise ImportError(
        f'Failed to import "{_module_name}". Did the C++ package not compile or install properly?',
        name=_module_name,
    )

__version__ = pycxxPROJECT.__version__
