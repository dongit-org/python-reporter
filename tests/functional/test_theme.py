from reporter import Reporter, ReportPage


def test_theme_operations(rc: Reporter) -> None:
    themes = rc.themes.list(include="pages")

    assert len(themes) == 1
    assert themes[0].name == "Reporter"
    assert len(themes[0].pages) == 2
    assert isinstance(themes[0].pages[0], ReportPage)
    assert themes[0].pages[0].name == "Front Page"
