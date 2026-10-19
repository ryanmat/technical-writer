# Description: Tests the template front matter schema and loader in
# Description: scripts/check_structure.py against inline YAML fixtures.
"""Tests for load_template and TemplateSpec."""

import re
import textwrap
from pathlib import Path

import pytest
from check_structure import AUDIENCES, DOMAINS, TemplateError, load_template

VALID = """\
---
type: task
domain: user documentation
default_audience: engineer
source: Grafana Writers' Toolkit task template
license: Apache-2.0
sections:
  - heading: Before you begin
    level: 2
    optional: true
  - heading: Steps
    level: 2
    evidence:
      pattern: 'https?://'
      missing: a reference URL for the command
  - heading_pattern: '^(Next steps|What next)$'
    level: 2
    optional: true
length_caps:
  engineer: 1200
  operator: 800
  executive: 400
banned_patterns:
  - pattern: '\\u2014'
    rule: no em dashes
---
# <TASK_NAME>

Body text the loader keeps apart from the front matter.
"""


def _write(tmp_path: Path, text: str, name: str = "task.md") -> Path:
    path = tmp_path / name
    path.write_text(textwrap.dedent(text))
    return path


def test_valid_template_parses_into_a_spec(tmp_path):
    spec = load_template(_write(tmp_path, VALID))
    assert spec.type == "task"
    assert [section.heading for section in spec.sections[:2]] == ["Before you begin", "Steps"]
    assert spec.sections[2].heading is None
    assert spec.sections[2].heading_pattern.match("Next steps")
    assert spec.sections[0].optional is True
    assert spec.sections[1].optional is False
    assert spec.sections[1].evidence.missing == "a reference URL for the command"
    assert spec.sections[1].evidence.pattern.search("see https://example.com")
    assert spec.default_audience in AUDIENCES
    assert set(spec.length_caps) <= set(AUDIENCES)
    assert spec.length_caps["operator"] == 800
    assert spec.procedure is False
    assert spec.summary_required is True
    assert spec.banned_patterns[0].rule == "no em dashes"
    assert spec.banned_patterns[0].pattern.search("a — b")


def test_missing_type_raises_naming_the_key(tmp_path):
    path = _write(tmp_path, VALID.replace("type: task\n", ""))
    with pytest.raises(TemplateError, match=r"\btype\b") as excinfo:
        load_template(path)
    assert str(path) in str(excinfo.value)


def test_duplicate_heading_at_the_same_level_raises_naming_the_heading(tmp_path):
    duplicated = VALID.replace(
        "  - heading: Steps\n    level: 2\n",
        "  - heading: Steps\n    level: 2\n  - heading: Steps\n    level: 2\n",
    )
    with pytest.raises(TemplateError, match="Steps"):
        load_template(_write(tmp_path, duplicated))


def test_length_cap_for_an_unknown_audience_lists_all_seven(tmp_path):
    with pytest.raises(TemplateError) as excinfo:
        load_template(_write(tmp_path, VALID.replace("  executive: 400\n", "  customer: 400\n")))
    message = str(excinfo.value)
    assert "customer" in message
    for audience in AUDIENCES:
        assert audience in message
    assert "operator" in message


@pytest.mark.parametrize(
    ("needle", "replacement", "expected"),
    [
        ("pattern: 'https?://'", "pattern: '(unclosed'", "Steps"),
        ("pattern: '\\u2014'", "pattern: '[bad'", "[bad"),
    ],
)
def test_invalid_regex_raises_naming_the_section_or_pattern(
    tmp_path, needle, replacement, expected
):
    assert needle in VALID, needle
    with pytest.raises(TemplateError, match=re.escape(expected)):
        load_template(_write(tmp_path, VALID.replace(needle, replacement)))


@pytest.mark.parametrize(
    ("needle", "replacement", "bad_key"),
    [
        ("summary_required", None, "summary_requried"),
        ("    optional: true\n", "    optinal: true\n", "optinal"),
        ("banned_patterns:\n", "banned_pattern:\n", "banned_pattern"),
        ("      missing: a reference URL", "      mising: a reference URL", "mising"),
        ("    rule: no em dashes", "    rules: no em dashes", "rules"),
    ],
)
def test_unknown_key_at_any_level_raises_naming_the_key(tmp_path, needle, replacement, bad_key):
    if replacement is None:
        text = VALID.replace("license: Apache-2.0\n", f"license: Apache-2.0\n{bad_key}: true\n")
    else:
        assert needle in VALID, needle
        text = VALID.replace(needle, replacement)
    with pytest.raises(TemplateError, match=re.escape(bad_key)):
        load_template(_write(tmp_path, text))


def test_procedure_true_without_procedure_section_raises(tmp_path):
    text = VALID.replace("license: Apache-2.0\n", "license: Apache-2.0\nprocedure: true\n")
    with pytest.raises(TemplateError, match="procedure_section"):
        load_template(_write(tmp_path, text))
    with_section = text.replace("procedure: true\n", "procedure: true\nprocedure_section: Steps\n")
    spec = load_template(_write(tmp_path, with_section))
    assert spec.procedure is True
    assert spec.procedure_section == "Steps"


def test_default_audience_outside_the_seven_raises_listing_them(tmp_path):
    text = VALID.replace("default_audience: engineer\n", "default_audience: customer\n")
    with pytest.raises(TemplateError) as excinfo:
        load_template(_write(tmp_path, text))
    message = str(excinfo.value)
    assert "default_audience" in message
    assert "customer" in message
    for audience in AUDIENCES:
        assert audience in message


def test_domain_outside_the_six_raises_listing_them(tmp_path):
    text = VALID.replace("domain: user documentation\n", "domain: marketing\n")
    with pytest.raises(TemplateError) as excinfo:
        load_template(_write(tmp_path, text))
    message = str(excinfo.value)
    assert "marketing" in message
    for domain in DOMAINS:
        assert domain in message
    assert len(DOMAINS) == 6


def test_section_label_must_be_a_non_empty_string_and_names_the_procedure_section(tmp_path):
    labelled = VALID.replace(
        "  - heading_pattern: '^(Next steps|What next)$'\n    level: 2\n",
        "  - heading_pattern: '^(Next steps|What next)$'\n    label: what comes next\n"
        "    level: 2\n",
    )
    assert labelled != VALID
    spec = load_template(_write(tmp_path, labelled))
    assert spec.sections[2].label == "what comes next"
    assert spec.sections[2].heading_pattern.pattern == "^(Next steps|What next)$"

    for bad in ("label: ''", "label: 3", "label: [a]"):
        text = labelled.replace("label: what comes next", bad)
        with pytest.raises(TemplateError, match="label"):
            load_template(_write(tmp_path, text))

    by_label = labelled.replace(
        "license: Apache-2.0\n",
        "license: Apache-2.0\nprocedure: true\nprocedure_section: what comes next\n",
    ).replace("    optional: true\nlength_caps", "length_caps")
    spec = load_template(_write(tmp_path, by_label))
    assert spec.procedure_section == "what comes next"
    by_pattern = by_label.replace(
        "procedure_section: what comes next", "procedure_section: '^(Next steps|What next)$'"
    )
    with pytest.raises(TemplateError, match="procedure_section"):
        load_template(_write(tmp_path, by_pattern))

    # two sections sharing a label at one level are as ambiguous as two sharing a heading;
    # procedure_section and the messages could not tell them apart
    shared = labelled.replace(
        "  - heading: Steps\n    level: 2\n",
        "  - heading: Steps\n    label: what comes next\n    level: 2\n",
    )
    assert shared != labelled
    with pytest.raises(TemplateError, match="what comes next"):
        load_template(_write(tmp_path, shared))


def test_section_max_words_is_a_mapping_of_audience_to_word_count(tmp_path):
    """A section may carry ``max_words``, words keyed by audience like
    ``length_caps``, for the GPAI form's recommended word count per field."""
    caps = "    max_words:\n      regulator: 20\n      executive: 5\n"
    capped = VALID.replace(
        "  - heading: Steps\n    level: 2\n", "  - heading: Steps\n    level: 2\n" + caps
    )
    assert capped != VALID
    spec = load_template(_write(tmp_path, capped))
    assert spec.sections[1].max_words == {"regulator": 20, "executive": 5}
    assert spec.sections[0].max_words == {}, "a section without the key has no per-section cap"

    for bad, match in (
        ("max_words: 20", "max_words"),
        ("max_words:\n      reader: 20", "reader"),
        ("max_words:\n      regulator: 0", "positive"),
        ("max_words:\n      regulator: twenty", "positive"),
        ("max_words:\n      regulator: true", "positive"),
    ):
        text = capped.replace("max_words:\n      regulator: 20\n      executive: 5", bad)
        assert text != capped
        with pytest.raises(TemplateError, match=match):
            load_template(_write(tmp_path, text))
