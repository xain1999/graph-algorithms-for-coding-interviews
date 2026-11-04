"""House style: printed code must fit the 7x10 page without wrapping."""
from pathlib import Path

import pytest

MAX_LINE = 70
ROOT = Path(__file__).resolve().parents[1]
PRINTED = [p for d in ("solutions", "templates", "snippets")
           for p in sorted((ROOT / d).glob("*.py"))]


@pytest.mark.parametrize("path", PRINTED, ids=lambda p: p.name)
def test_line_length(path):
    long = [(i, len(l)) for i, l in enumerate(path.read_text().splitlines(), 1) if len(l) > MAX_LINE]
    assert not long, f"{path.name}: lines over {MAX_LINE} chars: {long}"
