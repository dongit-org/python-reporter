from reporter import Reporter, FindingLayoutField


def test_finding_layout_operations(rc: Reporter) -> None:
    layouts = rc.finding_layouts.list(include="fields")

    assert len(layouts) == 1
    assert layouts[0].name == "Reporter"
    assert all(isinstance(field, FindingLayoutField) for field in layouts[0].fields)
    assert any(field.field == "description" for field in layouts[0].fields)
