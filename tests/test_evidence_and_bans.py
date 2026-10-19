# Description: Tests the evidence slot, banned pattern, and summary line checks in
# Description: scripts/check_structure.py, and the pass rule over their findings.
"""Tests for check_evidence, check_bans, check_summary, and passes."""

import textwrap
from pathlib import Path

import pytest
from check_structure import (
    GLOBAL_BANS,
    check_bans,
    check_evidence,
    check_summary,
    load_template,
    parse_document,
    passes,
)

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
    evidence:
      pattern: 'https?://'
      missing: a reference URL for the command
  - heading: Next steps
    level: 2
    optional: true
banned_patterns:
  - pattern: '\\bclick on\\b'
    rule: write click, not click on
---
# <TASK_NAME>
"""

DOCUMENT = """\
# Install the agent

Install the agent on one host.

## Steps

Run the installer from https://example.com/agent.

```bash
sudo apt install agent  # \u2014 this dash and the words simply and refer to are code
```

## Next steps

See the configuration reference.
"""


@pytest.fixture
def spec(tmp_path: Path):
    path = tmp_path / "task.md"
    path.write_text(textwrap.dedent(TEMPLATE))
    return load_template(path)


def test_filled_slot_yields_nothing_and_an_unverified_marker_is_info_and_still_passes(spec):
    assert check_evidence(parse_document(DOCUMENT), spec) == []

    marked = DOCUMENT.replace(
        "Run the installer from https://example.com/agent.",
        "Run the installer. [UNVERIFIED: the reference URL for the installer]",
    )
    findings = check_evidence(parse_document(marked), spec)
    assert [f.code for f in findings] == ["EVIDENCE_UNVERIFIED"]
    assert findings[0].severity == "info"
    assert findings[0].heading == "Steps"
    assert passes(findings) is True


def test_slot_with_neither_evidence_nor_marker_is_high_and_carries_the_missing_text(spec):
    bare = DOCUMENT.replace(
        "Run the installer from https://example.com/agent.", "Run the installer."
    )
    findings = check_evidence(parse_document(bare), spec)
    assert [f.code for f in findings] == ["EVIDENCE_MISSING"]
    assert findings[0].severity == "high"
    assert findings[0].heading == "Steps"
    assert "a reference URL for the command" in findings[0].message
    assert passes(findings) is False


@pytest.mark.parametrize(
    ("text", "rule_word"),
    [
        ("Install the agent \u2014 then start it.", "em dash"),
        ("Install the agent \u2013 then start it.", "en dash"),
        ("We recommend the stable channel.", "recommend"),
        ("Refer to the configuration reference.", "see"),
        ("Simply run the installer.", "subjective"),
    ],
)
def test_global_bans_are_low_with_line_and_rule_and_skip_fenced_code(spec, text, rule_word):
    doc = parse_document(DOCUMENT.replace("See the configuration reference.", text))
    findings = check_bans(doc, spec)
    assert [f.code for f in findings] == ["BANNED_PATTERN"]
    assert findings[0].severity == "low"
    assert findings[0].line == DOCUMENT.splitlines().index("See the configuration reference.") + 1
    assert rule_word in findings[0].rule
    assert passes(findings) is False

    clean = check_bans(parse_document(DOCUMENT), spec)
    assert clean == [], "the dash and words inside the fence must not be reported"


def test_inline_code_is_skipped_and_global_bans_carry_sources(spec):
    doc = parse_document(
        DOCUMENT.replace(
            "See the configuration reference.", "Run `simply --refer to` with no flags."
        )
    )
    assert check_bans(doc, spec) == []
    assert all(len(entry) == 3 and all(entry) for entry in GLOBAL_BANS)


def test_template_banned_pattern_is_reported_alongside_the_global_set(spec):
    doc = parse_document(
        DOCUMENT.replace("See the configuration reference.", "Then click on Save \u2014 wait.")
    )
    findings = check_bans(doc, spec)
    assert [f.code for f in findings] == ["BANNED_PATTERN", "BANNED_PATTERN"]
    assert {f.rule for f in findings} == {"no em dashes", "write click, not click on"}


def test_summary_line_must_be_exactly_one_sentence(spec):
    assert check_summary(parse_document(DOCUMENT), spec) == []

    two = DOCUMENT.replace(
        "Install the agent on one host.", "Install the agent on one host. It takes a minute."
    )
    findings = check_summary(parse_document(two), spec)
    assert [f.code for f in findings] == ["SUMMARY_MISSING"]
    assert findings[0].severity == "medium"
    assert findings[0].line == 3

    heading_first = DOCUMENT.replace("Install the agent on one host.\n\n", "")
    findings = check_summary(parse_document(heading_first), spec)
    assert [f.code for f in findings] == ["SUMMARY_MISSING"]
    assert findings[0].severity == "medium"


def test_summary_not_required_turns_the_check_off(tmp_path):
    path = tmp_path / "loose.md"
    path.write_text(
        textwrap.dedent(TEMPLATE).replace(
            "license: Apache-2.0\n", "license: Apache-2.0\nsummary_required: false\n"
        )
    )
    loose = load_template(path)
    two = DOCUMENT.replace(
        "Install the agent on one host.", "Install the agent on one host. It takes a minute."
    )
    assert check_summary(parse_document(two), loose) == []


def test_fence_lines_themselves_count_as_fenced():
    doc = parse_document(DOCUMENT)
    lines = DOCUMENT.splitlines()
    opening = lines.index("```bash") + 1
    closing = lines.index("```", opening) + 1
    assert {opening, closing} <= doc.fenced_lines
    assert all(opening <= n <= closing for n in doc.fenced_lines)


def test_evidence_under_a_subheading_of_the_section_fills_the_slot(spec):
    text = DOCUMENT.replace(
        "## Steps\n\nRun the installer from https://example.com/agent.",
        "## Steps\n\nRun the installer.\n\n### Reference\n\nThe installer is documented at "
        "https://example.com/agent.",
    )
    assert check_evidence(parse_document(text), spec) == []

    overrun = DOCUMENT.replace(
        "Run the installer from https://example.com/agent.", "Run it."
    ).replace("See the configuration reference.", "See https://example.com/agent to install.")
    assert [f.code for f in check_evidence(parse_document(overrun), spec)] == [
        "EVIDENCE_MISSING"
    ], "a URL in the next section must not fill the Steps slot"

    marked = text.replace(
        "The installer is documented at https://example.com/agent.",
        "[UNVERIFIED: the reference URL for the installer]",
    )
    findings = check_evidence(parse_document(marked), spec)
    assert [f.code for f in findings] == ["EVIDENCE_UNVERIFIED"]
    assert (
        findings[0].line
        == marked.splitlines().index("[UNVERIFIED: the reference URL for the installer]") + 1
    )


def test_link_destinations_and_bare_urls_are_not_prose_for_the_ban_scan(spec):
    doc = parse_document(
        DOCUMENT.replace(
            "See the configuration reference.",
            "See [the setup guide](https://example.com/docs/simple-setup) or "
            "https://example.com/docs/quickly-refer-to-this for details.",
        )
    )
    assert check_bans(doc, spec) == []

    flagged = parse_document(
        DOCUMENT.replace(
            "See the configuration reference.",
            "See [the simple setup guide](https://example.com/docs/setup).",
        )
    )
    findings = check_bans(flagged, spec)
    assert [f.rule for f in findings] == ["no subjective words"]


def test_every_marker_is_listed_at_info_wherever_it_sits(spec):
    """Finding: a marker in a section whose slot is already filled, in a
    section with no slot, or before the first heading was reported nowhere in the checker's
    JSON. Every marker is EVIDENCE_UNVERIFIED at info, with its line and enclosing heading."""
    marked = (
        DOCUMENT.replace(
            "Run the installer from https://example.com/agent.",
            "Run the installer from https://example.com/agent. [UNVERIFIED: the package name]",
        )
        .replace(
            "See the configuration reference.",
            "See the configuration reference. [UNVERIFIED: the reference URL]",
        )
        .replace(
            "Install the agent on one host.",
            "Install the agent on one host. [UNVERIFIED: the supported hosts]",
        )
    )
    findings = check_evidence(parse_document(marked), spec)
    assert [f.code for f in findings] == ["EVIDENCE_UNVERIFIED"] * 3
    assert {f.severity for f in findings} == {"info"}
    lines = marked.splitlines()
    headings = {f.line: f.heading for f in findings}
    assert headings == {
        lines.index("Install the agent on one host. [UNVERIFIED: the supported hosts]") + 1: (
            "Install the agent"
        ),
        lines.index(
            "Run the installer from https://example.com/agent. [UNVERIFIED: the package name]"
        )
        + 1: "Steps",
        lines.index("See the configuration reference. [UNVERIFIED: the reference URL]") + 1: (
            "Next steps"
        ),
    }
    assert all("[UNVERIFIED:" in f.message for f in findings)
    # the report writer prints the line in front of the message; the message does not repeat it
    assert not any(f.message.startswith("line ") for f in findings)
    assert passes(findings) is True


def test_a_marker_naming_the_slot_keyword_is_listed_like_any_other(tmp_path: Path):
    """Finding: a marker that names the missing fact with the slot's
    keyword satisfied the slot and was reported nowhere. Every marker is listed at info, so
    the section reads one EVIDENCE_UNVERIFIED whether or not its words match the slot."""
    path = tmp_path / "tutorial.md"
    path.write_text(
        textwrap.dedent(TEMPLATE)
        .replace("pattern: 'https?://'", "pattern: '(?i)\\bversion\\b'")
        .replace("missing: a reference URL for the command", "missing: the version tested")
    )
    spec = load_template(path)
    marked = DOCUMENT.replace(
        "Run the installer from https://example.com/agent.",
        "Run the installer. [UNVERIFIED: the version this tutorial was written against]",
    )
    findings = check_evidence(parse_document(marked), spec)
    assert [f.code for f in findings] == ["EVIDENCE_UNVERIFIED"]
    assert findings[0].heading == "Steps"

    filled = DOCUMENT.replace(
        "Run the installer from https://example.com/agent.",
        "Run the installer; these steps were tested on version 2.4.0.",
    )
    assert check_evidence(parse_document(filled), spec) == []

    bare = DOCUMENT.replace("Run the installer from https://example.com/agent.", "Run it.")
    assert [f.code for f in check_evidence(parse_document(bare), spec)] == ["EVIDENCE_MISSING"]


def test_markers_inside_fenced_code_are_not_findings_and_do_not_stand_in_for_a_slot(spec):
    """A marker in a code comment is not prose. It is not listed, and it does not stand in
    for an unfilled slot either, so the owner still sees the slot."""
    fenced = DOCUMENT.replace(
        "sudo apt install agent", "sudo apt install agent  # [UNVERIFIED: the package]"
    )
    assert check_evidence(parse_document(fenced), spec) == []

    unfilled = fenced.replace("Run the installer from https://example.com/agent.", "Run it.")
    findings = check_evidence(parse_document(unfilled), spec)
    assert [f.code for f in findings] == ["EVIDENCE_MISSING"]
    assert findings[0].heading == "Steps"


def test_the_dash_bans_cite_the_house_rule_and_splunk_not_google():
    """Finding: only Splunk's ruleset bans dashes; Google permits closed
    em dashes, so a review finding that passed the Google citation through was wrong."""
    sources = {pattern: source for pattern, _, source in GLOBAL_BANS}
    for dash in ("\u2014", "\u2013"):
        assert "house rule" in sources[dash]
        assert "Splunk Vale ruleset, Dashes.yml" in sources[dash]
        assert "Google" not in sources[dash]
