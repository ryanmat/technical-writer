# Description: Tests the shipped templates' front matter rules against documents the harness
# Description: fixtures do not cover: slot value forms and the task title exemptions.
"""Fix-round tests over the task and model card templates' slots and title pattern."""

import re
from pathlib import Path

from check_structure import check_document, load_template
from conftest import TEMPLATES_DIR

MODEL_CARD = TEMPLATES_DIR / "model-card.md"
TASK = TEMPLATES_DIR / "task.md"
REFERENCE = TEMPLATES_DIR / "reference.md"
TROUBLESHOOTING = TEMPLATES_DIR / "troubleshooting.md"
RELEASE_NOTES = TEMPLATES_DIR / "release-notes.md"
EVALS = Path(__file__).resolve().parents[1] / "evals"
REFERENCES = EVALS / "holdout"
MODEL_CARD_REFERENCE = REFERENCES / "model-card--relay-intent-classifier" / "reference.md"
TASK_REFERENCE = REFERENCES / "task--relay-alert-rule" / "reference.md"
REFERENCE_REFERENCE = EVALS / "cases" / "reference--relay-settings" / "reference.md"
TROUBLESHOOTING_REFERENCE = (
    EVALS / "cases" / "troubleshooting--relay-route-timeout" / "reference.md"
)
RELEASE_NOTES_REFERENCE = EVALS / "cases" / "release-notes--relay-2-5-0" / "reference.md"


def _codes(text: str, template: Path, heading: str | None = None) -> list[str]:
    findings = check_document(text, load_template(template))
    return [f.code for f in findings if heading is None or f.heading == heading]


def test_carbon_slot_is_not_filled_by_the_digit_in_co2eq_on_the_field_label():
    # Every marker is listed at info, so the slot is read with both of the
    # section's markers removed: the label's digit alone must leave the slot unfilled.
    unmarked = MODEL_CARD_REFERENCE.read_text(encoding="utf-8").replace(
        "- **Cloud Provider:** [UNVERIFIED: the cloud provider and compute region; the sources "
        "do not name them]",
        "- **Cloud Provider:** example.com cloud, region one",
    )
    assert "[UNVERIFIED: the cloud provider" not in unmarked
    carbon_marker = (
        "- **Carbon Emitted:** [UNVERIFIED: the carbon emitted in grams of CO2eq; the sources "
        "give hardware and hours only]"
    )
    assert carbon_marker in unmarked
    text = unmarked.replace(carbon_marker, "- **Carbon Emitted (grams of CO2eq):**")
    assert _codes(text, MODEL_CARD, "Environmental Impact") == ["EVIDENCE_MISSING"]

    filled = unmarked.replace(carbon_marker, "- **Carbon Emitted (grams of CO2eq):** 1200")
    assert _codes(filled, MODEL_CARD, "Environmental Impact") == []


def test_model_description_slot_needs_values_after_developed_by_and_license():
    reference = MODEL_CARD_REFERENCE.read_text(encoding="utf-8")
    assert _codes(reference, MODEL_CARD, "Model Description") == []

    empty = reference.replace("- **Developed by:** Northwind Labs", "- **Developed by:**")
    assert _codes(empty, MODEL_CARD, "Model Description") == ["EVIDENCE_MISSING"]

    marked = reference.replace(
        "- **License:** Apache-2.0", "- **License:** [UNVERIFIED: the license the registry names]"
    )
    assert _codes(marked, MODEL_CARD, "Model Description") == ["EVIDENCE_UNVERIFIED"]


def test_task_title_exempts_the_same_ing_words_as_the_heading_ban():
    reference = TASK_REFERENCE.read_text(encoding="utf-8")
    bring = reference.replace(
        "# Create an alert rule in Northwind Relay", "# Bring an alert rule back online"
    )
    assert "H1_PATTERN" not in _codes(bring, TASK)

    gerund = reference.replace(
        "# Create an alert rule in Northwind Relay", "# Creating an alert rule in Northwind Relay"
    )
    assert "H1_PATTERN" in _codes(gerund, TASK)


def test_reference_version_slot_is_not_filled_by_the_bare_phrase_taken_from():
    """Review Important: sourced from and taken from filled the slot with no source named,
    and the template's own example sentence for a missing version carried one."""
    reference = REFERENCE_REFERENCE.read_text(encoding="utf-8")
    title = "Alert rule settings in Northwind Relay"
    assert _codes(reference, REFERENCE, title) == []
    versioned = (
        "The values below hold for Northwind Relay 2.4.0, the release the rule editor's help "
        "text describes. Alert rules are available from 2.4.0."
    )
    assert versioned in reference
    # The level-one section spans the document, so the table's own marker would read as the
    # slot's; fill that cell to see the slot's verdict alone.
    cell = "[UNVERIFIED: the default delivery gap, which the help text does not show]"
    assert cell in reference
    unmarked = reference.replace(cell, "none")
    bare = unmarked.replace(
        versioned, "The values below hold for the release the settings list was taken from."
    )
    assert _codes(bare, REFERENCE, title) == ["EVIDENCE_MISSING"]
    sourced = unmarked.replace(
        versioned, "The values below hold for the release sourced from the rule editor."
    )
    assert _codes(sourced, REFERENCE, title) == ["EVIDENCE_MISSING"]
    marked = reference.replace(
        versioned,
        "The values below hold for the release the settings list was taken from. "
        "[UNVERIFIED: which release the settings list describes]",
    )
    assert _codes(marked, REFERENCE, title) == ["EVIDENCE_UNVERIFIED"]


def test_troubleshooting_output_slot_needs_an_output_sentence_right_after_the_fence():
    """Review Minor: an output word anywhere after a fence filled the slot, so step prose
    such as Return to the Routes page counted as a statement of output."""
    reference = TROUBLESHOOTING_REFERENCE.read_text(encoding="utf-8")
    assert _codes(reference, TROUBLESHOOTING, "Resolution") == []
    first = "The command prints `route billing: Active`."
    second = "The output reads `route billing: Active`, and the **Routes** page shows **Active**."
    assert first in reference and second in reference
    prose = reference.replace(first, "Return to the **Routes** page.").replace(
        second, "Return to the **Routes** page and check the state."
    )
    assert _codes(prose, TROUBLESHOOTING, "Resolution") == ["EVIDENCE_MISSING"]
    later = reference.replace(first, "Wait for the route to settle.").replace(
        second, "The page shows **Active** once the route settles."
    )
    assert _codes(later, TROUBLESHOOTING, "Resolution") == []
    far = reference.replace(first, "Wait for the route to settle.").replace(
        second, "Open the route again. The page shows **Active**."
    )
    assert _codes(far, TROUBLESHOOTING, "Resolution") == ["EVIDENCE_MISSING"]


def test_release_notes_date_slot_reads_the_full_iso_date_on_the_first_line_only():
    """The slot is the release line: the first line under the version heading, carrying the
    date as YYYY-MM-DD. A bare year, or the date on a later line, leaves it unfilled."""
    reference = RELEASE_NOTES_REFERENCE.read_text(encoding="utf-8")
    heading = "[2.5.0]"
    assert _codes(reference, RELEASE_NOTES, heading) == []
    release_line = "Released 2026-10-17. Northwind Relay follows Semantic Versioning."
    assert release_line in reference
    # The version section spans its entries, so the Fixed entry's marker would read as the
    # slot's; give that entry a key to see the slot's verdict alone.
    marker = "[UNVERIFIED: the issue or pull request that made this change]"
    assert marker in reference
    unmarked = reference.replace(marker, "(RELAY-407)")
    year_only = unmarked.replace(
        release_line, "Released in 2026. Northwind Relay follows Semantic Versioning."
    )
    assert _codes(year_only, RELEASE_NOTES, heading) == ["EVIDENCE_MISSING"]
    later_line = unmarked.replace(
        release_line, "Northwind Relay follows Semantic Versioning.\n\nReleased 2026-10-17."
    )
    assert _codes(later_line, RELEASE_NOTES, heading) == ["EVIDENCE_MISSING"]
    marked = reference.replace(
        release_line,
        "[UNVERIFIED: the release date] Northwind Relay follows Semantic Versioning.",
    )
    assert _codes(marked, RELEASE_NOTES, heading) == ["EVIDENCE_UNVERIFIED"]


def test_postmortem_impact_slot_reads_any_counted_noun_and_a_hyphenated_duration():
    """Fix round, the reviewer's Important: the Impact slot took its count
    units from the relay case, so a postmortem counting orders or jobs failed at high
    severity, and "a 38-minute outage" missed the duration. A duration in any form and a
    number with any noun that is not a time unit fill the slot; a duration alone does not."""
    postmortem = TEMPLATES_DIR / "postmortem.md"
    body = "\n\n".join(
        [
            "# Checkout outage on 2026-10-03",
            "Checkout failed for 38 minutes because a pool filled.",
            "## Summary\n\nIt failed.",
            "## Impact\n\n{impact}",
            "## Root causes and trigger\n\nA pool.",
            "## Timeline and recovery\n\n- 2026-10-03T14:02Z: start.",
            "## Detection\n\nAn alert.",
            "## Action items\n\n- Fix the pool (owner: team, priority: P1, SHOP-1).",
            "## Lessons learned\n\nNone.\n",
        ]
    )
    for impact in (
        "Checkout failed for 38 minutes and 1,240 orders were rejected.",
        "A 38-minute outage rejected 1,240 orders in two regions.",
        "For 2 hours 17 jobs waited.",
    ):
        assert _codes(body.format(impact=impact), postmortem, "Impact") == [], impact
    for impact in (
        "Checkout failed for 38 minutes.",
        "Checkout failed for 38 minutes and then for 12 minutes more.",
        "Orders were rejected for 1,240 of them.",
        "Checkout failed for 38 minutes on 2026-10-03 from 14:02 UTC until 14:40 UTC.",
        "Delivery stopped for 42 minutes, from 14:02 to 14:44 UTC.",
        "Delivery stopped on 2026-10-03 for 42 minutes.",
        "Delivery stopped for 42 minutes and p99 rose to 120 ms.",
    ):
        assert _codes(body.format(impact=impact), postmortem, "Impact") == ["EVIDENCE_MISSING"], (
            impact
        )


def test_an_algorithm_or_standard_name_is_not_an_entry_key():
    """Fix round, a review Minor: the entry identifier alternative also matched
    SHA-256 and UTF-8, so a Security entry naming one passed the rule with no issue, pull
    request or commit. A letter prefix that is an algorithm or standard name is not a key; a
    tracker key, an issue number and a commit hash still are, in both templates that share
    the rule."""
    reference = RELEASE_NOTES_REFERENCE.read_text(encoding="utf-8")
    marker = "[UNVERIFIED: the issue or pull request that made this change]"
    assert marker in reference
    # a banned-pattern finding carries the line, not the section, so these read every code
    for key in ("(RELAY-407)", "(#407)", "(3f2a9c1)"):
        assert "BANNED_PATTERN" not in _codes(reference.replace(marker, key), RELEASE_NOTES), key
    for name in ("SHA-256", "UTF-8", "CVE-1900-0001", "RFC-9110", "1048576 bytes"):
        unkeyed = reference.replace(marker, f"(moved to {name})")
        assert "BANNED_PATTERN" in _codes(unkeyed, RELEASE_NOTES), name
    changelog = TEMPLATES_DIR / "changelog-entry.md"
    entry = (
        "# Relay changelog\n\nAll notable changes to Relay.\n\n## [2.5.1] - 2026-10-17\n\n"
        "### Security\n\n- Digests use {key}.\n"
    )
    unkeyed = _codes(entry.format(key="SHA-256"), changelog)
    assert "BANNED_PATTERN" in unkeyed and "EVIDENCE_MISSING" in unkeyed, unkeyed
    keyed = _codes(entry.format(key="SHA-256 (RELAY-431)"), changelog)
    assert "BANNED_PATTERN" not in keyed and "EVIDENCE_MISSING" not in keyed, keyed


def test_ing_nouns_a_product_area_uses_are_not_gerund_headings():
    """User-docs pass: the concept template read ## Timing as a gerund heading. The
    exemption list is the same in the concept, reference and troubleshooting templates."""
    concept = TEMPLATES_DIR / "concept.md"
    reference = EVALS / "cases" / "concept--relay-routing-model" / "reference.md"
    text = reference.read_text(encoding="utf-8")
    assert "BANNED_PATTERN" not in _codes(text, concept)
    for noun in ("Timing", "Scheduling", "Batching", "Routing"):
        with_noun = text.replace(
            "\n## ", f"\n## {noun}\n\nOne sentence on {noun.lower()}.\n\n## ", 1
        )
        assert with_noun != text
        codes = _codes(with_noun, concept)
        assert "BANNED_PATTERN" not in codes, (noun, codes)
    gerund = text.replace("\n## ", "\n## Sending a message\n\nOne sentence.\n\n## ", 1)
    assert "BANNED_PATTERN" in _codes(gerund, concept)
    for template in (REFERENCE, TROUBLESHOOTING):
        spec = load_template(template)
        exempt = [b for b in spec.banned_patterns if "Timing" in b.pattern.pattern]
        assert exempt, f"{template.name}: the -ing heading ban does not exempt Timing"
        assert "Timing" in spec.h1_pattern.pattern, f"{template.name}: the h1_pattern does not"


def test_task_family_title_may_carry_a_comma_after_the_first_verb():
    """User-docs pass: a multiple-task title in the form Install, start, and verify
    the agent failed the task-family H1 pattern on the comma after its first word."""
    for name in ("task.md", "multiple-task-procedure.md", "tutorial.md"):
        template = TEMPLATES_DIR / name
        spec = load_template(template)
        for title in ("Install, start, and verify the Relay agent", "Install the agent"):
            assert spec.h1_pattern.search(title), (name, title)
        for title in ("Installing the agent", "The agent install", "Install", "Install,"):
            assert not spec.h1_pattern.search(title), (name, title)


PRIVACY_NOTICE = TEMPLATES_DIR / "privacy-notice.md"
PRIVACY_NOTICE_REFERENCE = EVALS / "cases" / "privacy-notice--relay-account" / "reference.md"


def test_privacy_notice_qualifier_ban_spares_the_month_may():
    """Review Important: the ban's case-insensitive flag covers the four qualifiers
    only, so the month May passes while a lowercase may, and a capitalised Some, are banned."""
    reference = PRIVACY_NOTICE_REFERENCE.read_text(encoding="utf-8")
    assert "BANNED_PATTERN" not in _codes(reference, PRIVACY_NOTICE)
    dated = reference + "\n## Changes to this notice\n\nLast updated 12 May 2026.\n"
    assert "BANNED_PATTERN" not in _codes(dated, PRIVACY_NOTICE)
    hedged = reference.replace("We keep logs for 13 months.", "We may keep logs for 13 months.")
    assert hedged != reference
    assert "BANNED_PATTERN" in _codes(hedged, PRIVACY_NOTICE)
    capitalised = reference.replace("We keep logs for 13 months.", "Some logs are kept.")
    assert "BANNED_PATTERN" in _codes(capitalised, PRIVACY_NOTICE)


DPIA = TEMPLATES_DIR / "data-protection-impact-assessment.md"
DPIA_REFERENCE = EVALS / "cases" / "dpia--relay-analytics" / "reference.md"
PROCESSING = "Describe the processing"


def test_dpia_processing_slot_needs_nature_scope_context_and_purpose_all_stated():
    """Review Minor: the slot was filled by any one of the four
    words while its missing text asks for all four. The reference states each; a section
    with one of them cut is the finding, and one carrying only context and purpose is too."""
    # The marker is stripped first: a marked section reads as unverified, never as missing.
    reference = re.sub(r"\[UNVERIFIED:[^\]]*\] ?", "", DPIA_REFERENCE.read_text(encoding="utf-8"))
    assert "EVIDENCE_MISSING" not in _codes(reference, DPIA, PROCESSING)
    for word in ("nature", "scope", "context", "purpose"):
        cut = reference.replace(f"The {word}", "The thing", 1)
        assert cut != reference, f"the reference states no {word}"
        assert "EVIDENCE_MISSING" in _codes(cut, DPIA, PROCESSING), word
    two_words = (
        "# Data protection impact assessment: Unit\n\nOne sentence.\n\n"
        "## Identify the need for a DPIA\n\nNeeded.\n\n"
        "## Describe the processing\n\nThe purpose is billing and the context is work.\n\n"
    )
    assert "EVIDENCE_MISSING" in _codes(two_words, DPIA, PROCESSING)
