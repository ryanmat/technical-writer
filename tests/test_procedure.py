# Description: Tests the procedure rules in scripts/check_structure.py: step length, one
# Description: action per step, the stem sentence, and admonition placement.
"""Tests for check_procedure and the procedure_section loader guard."""

import textwrap
from pathlib import Path

import pytest
from check_structure import (
    TemplateError,
    check_document,
    check_procedure,
    load_template,
    parse_document,
)

TEMPLATE = """\
---
type: task
domain: user documentation
default_audience: engineer
source: Grafana Writers' Toolkit task template
license: Apache-2.0
procedure: true
procedure_section: Steps
sections:
  - heading: Before you begin
    level: 2
    optional: true
  - heading: Steps
    level: 2
---
# <TASK_NAME>
"""

DOCUMENT = """\
# Install the agent

Install the agent on one host.

## Before you begin

You need root on the host.

## Steps

To install the agent:

1. Open a terminal on the host.
2. Run the installer.

   ```bash
   sudo apt install agent  # 1. not a step, and these words never count against any cap
   ```

   The prompt returns with no error.

**Caution:** The next step restarts the host and drops every open session.

3. Restart the host.
"""

PROCEDURE_CODES = {"STEP_TOO_LONG", "STEP_TOO_MANY_SENTENCES", "STEM_MISSING", "WARNING_AFTER_STEP"}


def _spec(tmp_path: Path, text: str = TEMPLATE, name: str = "task.md"):
    path = tmp_path / name
    path.write_text(textwrap.dedent(text))
    return load_template(path)


def test_conforming_procedure_yields_no_findings(tmp_path):
    spec = _spec(tmp_path)
    assert check_procedure(parse_document(DOCUMENT), spec) == []
    assert check_document(DOCUMENT, spec) == []


def test_step_first_sentence_over_twenty_words_is_medium_with_its_line(tmp_path):
    long_step = (
        "Open a terminal on the host that will run the agent and keep it open until "
        "all the following steps complete."
    )
    assert len(long_step.rstrip(".").split()) == 21
    text = DOCUMENT.replace("Open a terminal on the host.", long_step)
    findings = check_procedure(parse_document(text), _spec(tmp_path))
    assert [f.code for f in findings] == ["STEP_TOO_LONG"]
    assert findings[0].severity == "medium"
    assert findings[0].line == DOCUMENT.splitlines().index("1. Open a terminal on the host.") + 1
    assert "21" in findings[0].message

    twenty = (
        "Open a terminal on the host that runs the agent and keep it open until the last "
        "step completes here."
    )
    assert len(twenty.rstrip(".").split()) == 20
    text = DOCUMENT.replace("Open a terminal on the host.", twenty)
    assert check_procedure(parse_document(text), _spec(tmp_path)) == []


def test_step_with_three_sentences_is_medium(tmp_path):
    text = DOCUMENT.replace(
        "Open a terminal on the host.", "Open a terminal. Check the shell. Note the version."
    )
    findings = check_procedure(parse_document(text), _spec(tmp_path))
    assert [f.code for f in findings] == ["STEP_TOO_MANY_SENTENCES"]
    assert findings[0].severity == "medium"
    assert findings[0].line == DOCUMENT.splitlines().index("1. Open a terminal on the host.") + 1


def test_an_unverified_marker_in_a_step_is_neither_a_sentence_nor_words(tmp_path):
    """User-docs pass: three of four checker failures counted the marker after a
    result sentence as a third sentence. The marker names a missing fact; it is not prose."""
    marked = DOCUMENT.replace(
        "   The prompt returns with no error.",
        "   The prompt returns with no error. [UNVERIFIED: the exact text the installer prints]",
    )
    assert marked != DOCUMENT
    assert check_procedure(parse_document(marked), _spec(tmp_path)) == []

    twenty = (
        "Open a terminal on the host that runs the agent and keep it open until the last "
        "step completes here"
    )
    assert len(twenty.split()) == 20
    inline = DOCUMENT.replace(
        "Open a terminal on the host.", f"{twenty} [UNVERIFIED: which shell the host runs]."
    )
    assert check_procedure(parse_document(inline), _spec(tmp_path)) == []

    three = DOCUMENT.replace(
        "Open a terminal on the host.",
        "Open a terminal. Check the shell. Note the version. [UNVERIFIED: the shell]",
    )
    findings = check_procedure(parse_document(three), _spec(tmp_path))
    assert [f.code for f in findings] == ["STEP_TOO_MANY_SENTENCES"]
    assert "3 sentences" in findings[0].message


def test_first_list_without_a_stem_sentence_beginning_with_to_is_medium(tmp_path):
    spec = _spec(tmp_path)
    no_stem = DOCUMENT.replace("To install the agent:\n\n", "")
    findings = check_procedure(parse_document(no_stem), spec)
    assert [f.code for f in findings] == ["STEM_MISSING"]
    assert findings[0].severity == "medium"
    assert findings[0].heading == "Steps"

    wrong_stem = DOCUMENT.replace("To install the agent:", "Follow these steps.")
    findings = check_procedure(parse_document(wrong_stem), spec)
    assert [f.code for f in findings] == ["STEM_MISSING"]
    stem_line = DOCUMENT.splitlines().index("To install the agent:") + 1
    assert findings[0].line == stem_line


def test_admonition_after_the_last_step_is_medium_and_procedure_false_checks_nothing(tmp_path):
    text = DOCUMENT + "\n**Warning:** Do not unplug the host while it restarts.\n"
    findings = check_procedure(parse_document(text), _spec(tmp_path))
    assert [f.code for f in findings] == ["WARNING_AFTER_STEP"]
    assert findings[0].severity == "medium"
    assert findings[0].line == len(DOCUMENT.splitlines()) + 2

    plain = _spec(tmp_path, TEMPLATE.replace("procedure: true\n", "procedure: false\n"), "plain.md")
    broken = text.replace("To install the agent:", "Follow these steps.").replace(
        "Open a terminal on the host.", "Open a terminal. Check the shell. Note the version."
    )
    assert check_procedure(parse_document(broken), plain) == []
    assert not PROCEDURE_CODES & {f.code for f in check_document(broken, plain)}
    assert PROCEDURE_CODES & {f.code for f in check_document(broken, _spec(tmp_path))}


def test_procedure_section_must_name_a_declared_heading(tmp_path):
    with pytest.raises(TemplateError, match="Install") as excinfo:
        _spec(
            tmp_path,
            TEMPLATE.replace("procedure_section: Steps\n", "procedure_section: Install\n"),
        )
    assert "Steps" in str(excinfo.value)


def test_fenced_lines_in_the_steps_section_are_never_steps_or_admonitions(tmp_path):
    text = DOCUMENT + textwrap.dedent(
        """
        ```text
        4. Open a terminal. Check the shell. Note the version and the host and the user and more.
        **Warning:** inside a fence this is output, not an admonition.
        ```
        """
    )
    assert check_procedure(parse_document(text), _spec(tmp_path)) == []


def test_indented_continuation_lines_belong_to_their_step(tmp_path):
    text = DOCUMENT.replace(
        "3. Restart the host.\n",
        "3. Restart the host.\n   Wait for the login prompt. Log in again.\n",
    )
    findings = check_procedure(parse_document(text), _spec(tmp_path))
    assert [f.code for f in findings] == ["STEP_TOO_MANY_SENTENCES"]
    assert findings[0].line == DOCUMENT.splitlines().index("3. Restart the host.") + 1


def test_steps_subdivided_into_h3s_are_still_checked_and_the_h3_is_never_the_stem(tmp_path):
    text = DOCUMENT.replace(
        "## Steps\n\nTo install the agent:\n\n1. Open a terminal on the host.\n",
        "## Steps\n\n### Install\n\nTo install the agent:\n\n"
        "1. Open a terminal. Check the shell. Note the version.\n",
    )
    spec = _spec(tmp_path)
    findings = check_procedure(parse_document(text), spec)
    assert [f.code for f in findings] == ["STEP_TOO_MANY_SENTENCES"]
    assert (
        findings[0].line
        == text.splitlines().index("1. Open a terminal. Check the shell. Note the version.") + 1
    )

    stem_under_h3 = DOCUMENT.replace(
        "## Steps\n\nTo install the agent:\n\n",
        "## Steps\n\nTo install the agent:\n\n### Install\n\n",
    )
    assert check_procedure(parse_document(stem_under_h3), spec) == []


def test_stem_must_be_its_own_paragraph_and_end_in_a_colon(tmp_path):
    """Ruled 2026-10-18 13:08 EDT: the stem is the whole paragraph before step 1,
    begins with To and ends in a colon or a period (the holdout task reference carries
    Grafana's period form); a stem with no terminal punctuation, or one sharing its paragraph
    with a warning sentence, is STEM_MISSING, as the runbook case's mitigation-stem grader
    read the shared paragraph."""
    spec = _spec(tmp_path)
    assert check_procedure(parse_document(DOCUMENT), spec) == []
    period = DOCUMENT.replace("To install the agent:", "To install the agent, follow these steps.")
    assert check_procedure(parse_document(period), spec) == []

    unpunctuated = DOCUMENT.replace(
        "To install the agent:", "To install the agent, follow these steps"
    )
    findings = check_procedure(parse_document(unpunctuated), spec)
    assert [f.code for f in findings] == ["STEM_MISSING"]
    assert "colon or a period" in findings[0].message

    shared = DOCUMENT.replace(
        "To install the agent:", "The installer needs ten minutes. To install the agent:"
    )
    findings = check_procedure(parse_document(shared), spec)
    assert [f.code for f in findings] == ["STEM_MISSING"]
    assert "paragraph" in findings[0].message

    own_paragraph = DOCUMENT.replace(
        "To install the agent:", "The installer needs ten minutes.\n\nTo install the agent:"
    )
    assert check_procedure(parse_document(own_paragraph), spec) == []


def test_a_caution_before_the_first_step_is_not_read_as_the_stem(tmp_path):
    text = DOCUMENT.replace(
        "To install the agent:\n\n1.",
        "To install the agent:\n\n"
        "**Caution:** The installer overwrites an existing agent configuration.\n\n1.",
    )
    assert check_procedure(parse_document(text), _spec(tmp_path)) == []


# ---- a procedure section named by its heading_pattern -----------------------------

MULTI_TEMPLATE = """\
---
type: multiple-task procedure
domain: user documentation
default_audience: engineer
source: Grafana Writers' Toolkit multiple-tasks template
license: Apache-2.0
procedure: true
procedure_section: '^(?!Before you begin$).+'
sections:
  - heading: Before you begin
    level: 2
    optional: true
  - heading_pattern: '^(?!Before you begin$).+'
    level: 2
---
# <TASK_NAME>
"""

MULTI_DOCUMENT = """\
# Install and start the agent

Install the agent on one host and start it.

## Before you begin

You need root on the host.

## Install the agent

To install the agent:

1. Open a terminal on the host.
2. Run the installer.

## Start the agent

Run the service.

1. Start the service.
2. Check its status.
"""


def test_procedure_section_may_name_a_pattern_section_and_every_matching_heading_is_checked(
    tmp_path,
):
    spec = _spec(tmp_path, MULTI_TEMPLATE, "multi.md")
    assert spec.procedure_section == "^(?!Before you begin$).+"
    findings = check_procedure(parse_document(MULTI_DOCUMENT), spec)
    assert [(f.code, f.heading) for f in findings] == [("STEM_MISSING", "Start the agent")]
    assert findings[0].line == MULTI_DOCUMENT.splitlines().index("Run the service.") + 1

    both_good = MULTI_DOCUMENT.replace("Run the service.", "To start the agent:")
    assert check_procedure(parse_document(both_good), spec) == []
    assert check_document(both_good, spec) == []
