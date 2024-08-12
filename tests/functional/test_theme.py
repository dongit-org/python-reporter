import pytest

import reporter
from reporter import Reporter


def test_theme_operations(rc: Reporter) -> None:
    themes = rc.themes.list()

    assert len(themes) > 0 and themes[0].name == "Reporter"
