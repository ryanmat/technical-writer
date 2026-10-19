# Description: Tests Markdown parsing and the section checks in scripts/check_structure.py
# Description: against a small task-shaped template fixture and inline Markdown documents.
"""Tests for parse_document and check_sections."""

import textwrap
from pathlib import Path

import pytest
from check_structure import check_sections, load_template, parse_document

TEMPLATE = """\
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
  - heading_pattern: '^(Next steps|What next)$'
    level: 2
---
# <TASK_NAME>
"""

CONFORMING = """\
# Install the agent

Install the agent on one host.

## Before you begin

You need root on the host.

## Steps

```bash
# heading-looking comment inside a fence
sudo apt install agent
```

~~~
# another fenced heading, tilde style
~~~

## Next steps

See the configuration reference.
"""


@pytest.fixture
def spec(tmp_path: Path):
    path = tmp_path / "task.md"
    path.write_text(textwrap.dedent(TEMPLATE))
    return load_template(path)


def test_conforming_document_yields_no_findings_and_fenced_headings_are_skipped(spec):
    doc = parse_document(CONFORMING)
    assert [heading.text for heading in doc.headings] == [
        "Install the agent",
        "Before you begin",
        "Steps",
        "Next steps",
    ]
    assert [heading.level for heading in doc.headings] == [1, 2, 2, 2]
    assert doc.headings[2].body.strip().startswith("```bash")
    assert check_sections(doc, spec) == []


def test_missing_required_section_is_high_and_names_the_heading(spec):
    text = CONFORMING.replace("## Steps\n", "").replace("sudo apt install agent\n", "")
    findings = check_sections(parse_document(text), spec)
    assert [f.code for f in findings] == ["SECTION_MISSING"]
    assert findings[0].severity == "high"
    assert findings[0].heading == "Steps"
    assert "Steps" in findings[0].message


def test_swapped_required_sections_are_medium_and_name_both(spec):
    text = (
        "# Install the agent\n\nInstall the agent on one host.\n\n"
        "## Next steps\n\nSee the reference.\n\n"
        "## Steps\n\nRun the installer.\n"
    )
    findings = check_sections(parse_document(text), spec)
    assert [f.code for f in findings] == ["SECTION_ORDER"]
    assert findings[0].severity == "medium"
    assert "Steps" in findings[0].message
    assert "Next steps" in findings[0].message


def test_unknown_heading_is_medium_with_its_line_number(spec):
    text = CONFORMING + "\n## Appendix\n\nExtra material.\n"
    findings = check_sections(parse_document(text), spec)
    assert [f.code for f in findings] == ["SECTION_UNKNOWN"]
    assert findings[0].severity == "medium"
    assert findings[0].heading == "Appendix"
    assert findings[0].line == CONFORMING.count("\n") + 2
    assert findings[0].to_dict()["line"] == findings[0].line


def test_two_h1s_or_no_h1_yield_h1_count_at_medium(spec):
    two = CONFORMING + "\n# A second title\n"
    findings = check_sections(parse_document(two), spec)
    assert [f.code for f in findings] == ["H1_COUNT"]
    assert findings[0].severity == "medium"
    assert "2" in findings[0].message

    none = CONFORMING.replace("# Install the agent\n", "")
    findings = check_sections(parse_document(none), spec)
    assert [f.code for f in findings] == ["H1_COUNT"]
    assert findings[0].severity == "medium"
    assert "0" in findings[0].message


def test_single_h1_that_misses_the_h1_pattern_is_h1_pattern_at_medium(tmp_path):
    path = tmp_path / "verb-first.md"
    path.write_text(
        textwrap.dedent(TEMPLATE).replace(
            "license: Apache-2.0\n", "license: Apache-2.0\nh1_pattern: '^(Install|Configure)\\b'\n"
        )
    )
    spec = load_template(path)
    assert check_sections(parse_document(CONFORMING), spec) == []

    noun_title = CONFORMING.replace("# Install the agent", "# Agent installation")
    findings = check_sections(parse_document(noun_title), spec)
    assert [f.code for f in findings] == ["H1_PATTERN"]
    assert findings[0].severity == "medium"
    assert findings[0].line == 1
    assert "Agent installation" in findings[0].message

    two_titles = noun_title + "\n# Second title\n"
    codes = [f.code for f in check_sections(parse_document(two_titles), spec)]
    assert "H1_COUNT" in codes
    assert "H1_PATTERN" not in codes, "a count problem is H1_COUNT's alone"


def test_a_labelled_pattern_section_is_named_by_its_label_in_messages(tmp_path: Path):
    """Finding: a section declared by heading_pattern was named by its
    regex in SECTION_MISSING and SECTION_ORDER messages, which review mode passes to the
    reader. An optional label key names it instead."""
    path = tmp_path / "task.md"
    path.write_text(
        textwrap.dedent(TEMPLATE).replace(
            "  - heading_pattern: '^(Next steps|What next)$'\n    level: 2\n",
            "  - heading_pattern: '^(Next steps|What next)$'\n    label: the next steps section\n"
            "    level: 2\n",
        )
    )
    spec = load_template(path)
    assert spec.sections[2].label == "the next steps section"
    assert spec.sections[0].label == "Before you begin"

    missing = CONFORMING.replace("## Next steps\n\nSee the configuration reference.\n", "")
    findings = check_sections(parse_document(missing), spec)
    assert [f.code for f in findings] == ["SECTION_MISSING"]
    assert findings[0].heading == "the next steps section"
    assert findings[0].message == "required section 'the next steps section' is missing"
    assert "^(Next steps" not in findings[0].message

    swapped = (
        CONFORMING.replace("## Steps\n", "## Later\n")
        .replace(
            "## Next steps\n\nSee the configuration reference.\n",
            "## Next steps\n\nSee the configuration reference.\n\n## Steps\n\nRun it.\n",
        )
        .replace("## Later\n", "")
    )
    findings = check_sections(parse_document(swapped), spec)
    order = [f for f in findings if f.code == "SECTION_ORDER"]
    assert len(order) == 1
    assert "the next steps section" in order[0].message
    assert "^(Next steps" not in order[0].message
