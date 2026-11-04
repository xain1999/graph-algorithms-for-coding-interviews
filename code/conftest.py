# Lets tests import `solutions.<module>` when pytest runs from code/.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import inspect

import pytest


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "timing: checks a running time; depends on the machine")


def pytest_collection_modifyitems(items):
    """Mark every test that measures time, so correctness can be run on
    its own:  python -m pytest -m "not timing"."""
    for item in items:
        func = getattr(item, "function", None)
        try:
            source = inspect.getsource(func) if func else ""
        except (OSError, TypeError):
            source = ""
        if "perf_counter" in source:
            item.add_marker(pytest.mark.timing)
