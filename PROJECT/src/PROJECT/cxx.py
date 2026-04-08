"""
PROJECT C++ module loader

Import object from the PROJECT C++ module
"""

__author__ = "AUTHOR"
__contact__ = "EMAIL"

import importlib
import logging

_log = logging.getLogger("PROJECT.cxx")
_module_name = ".cxxPROJECT"

try:
    _log.info(f"Importing {_module_name}")
    pycxx = importlib.import_module(_module_name, package="PROJECT")
except ImportError:
    _log.error(f"Failed to import {_module_name}")
    raise ImportError(
        f'Failed to import "{_module_name}". Did the C++ package not compile or install properly?',
        name=_module_name,
    )

__version__ = pycxx.__version__
globals().update(
    {
        symbol: getattr(pycxx, symbol)
        for symbol in dir(pycxx)
        if not symbol.startswith("_")
    }
)
