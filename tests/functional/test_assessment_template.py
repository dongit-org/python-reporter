import pytest

import reporter
from reporter import Reporter

from .utils import Artisan


def test_assessment_template_crud(rc: Reporter) -> None:
    languages = rc.languages.list()
    primary_language = languages[0]

    template = rc.assessment_templates.create(
        {
            "primary_language_id": primary_language.id,
            "name": "test_assessment_template_crud",
            "enabled": True,
        }
    )

    assert template in rc.assessment_templates.list(filter={"id": template.id})

    rc.assessment_templates.update(template.id, {"name": "test_renamed"})
    gotten = rc.assessment_templates.get(template.id)
    assert gotten.name == "test_renamed"
    assert gotten.enabled is True

    rc.assessment_templates.delete(template.id)
    with pytest.raises(reporter.ReporterHttpError) as e:
        rc.assessment_templates.get(template.id)
        assert e.value.response_code == 404


def test_assessment_template_translations(rc: Reporter, artisan: Artisan) -> None:
    artisan.execute(
        "\\App\\Models\\Language::firstOrCreate("
        '["language" => "nl"], '
        '["name" => "Dutch", "translated_name" => "Nederlands"]'
        ");"
    )

    languages = rc.languages.list()
    primary_language = next(lang for lang in languages if lang.id == "en")
    other_language = next(lang for lang in languages if lang.id == "nl")

    template = rc.assessment_templates.create(
        {
            "primary_language_id": primary_language.id,
            "name": "test_translations_primary",
            "enabled": True,
        }
    )

    translated = rc.assessment_templates.add_translation(
        template.id,
        {
            "language_id": other_language.id,
            "source_language_id": primary_language.id,
        },
    )
    assert other_language.id in translated.translations

    rc.assessment_templates.update(
        template.id,
        {"language_id": other_language.id, "name": "test_translations_other"},
    )
    in_other = rc.assessment_templates.get(
        template.id, query_data={"language_id": other_language.id}
    )
    assert in_other.name == "test_translations_other"

    after_destroy = rc.assessment_templates.destroy_translation(
        template.id, other_language.id
    )
    assert other_language.id not in after_destroy.translations

    rc.assessment_templates.delete(template.id)


def test_assessment_section_template_crud(rc: Reporter) -> None:
    languages = rc.languages.list()
    primary_language = languages[0]

    template = rc.assessment_templates.create(
        {
            "primary_language_id": primary_language.id,
            "name": "test_section_template_crud",
            "enabled": True,
        }
    )

    base_attrs = {
        "can_have_findings": True,
        "finding_is_required": False,
        "report_section_visibility": 1,
        "is_visible_in_assessment_overview": True,
        "text_editable_with_permission": False,
        "force_page_break_after_section": False,
        "management_report_section_visibility": 1,
        "review_status": 0,
        "is_published": True,
    }

    section_a = template.sections.create({"name": "Section A", **base_attrs})
    section_b = template.sections.create({"name": "Section B", **base_attrs})

    listed = rc.assessment_section_templates.list(
        filter={"assessment_template_id": template.id}
    )
    listed_ids = {s.id for s in listed}
    assert {section_a.id, section_b.id} <= listed_ids

    gotten = rc.assessment_section_templates.get(section_a.id)
    assert gotten.name == "Section A"

    rc.assessment_section_templates.update(section_a.id, {"name": "Section A renamed"})
    assert rc.assessment_section_templates.get(section_a.id).name == "Section A renamed"

    template.sections.reorder(
        {
            "sections": [
                {"id": section_b.id, "children": []},
                {"id": section_a.id, "children": []},
            ]
        }
    )
    template_with_sections = rc.assessment_templates.get(
        template.id, include="sections"
    )
    ordered = sorted(template_with_sections.sections, key=lambda s: s.order)
    assert [s.id for s in ordered] == [section_b.id, section_a.id]

    rc.assessment_section_templates.delete(section_a.id)
    remaining = rc.assessment_section_templates.list(
        filter={"assessment_template_id": template.id}
    )
    assert section_a.id not in {s.id for s in remaining}
    assert section_b.id in {s.id for s in remaining}

    rc.assessment_templates.delete(template.id)
