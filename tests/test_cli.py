# Description: Tests the audience length cap and the JSON command line of
# Description: scripts/check_structure.py, the latter through subprocess like the graders use it.
"""Tests for check_length, check_document, and main."""

import json
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest
from check_structure import check_document, check_length, load_template, parse_document

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_structure.py"

TEMPLATE = """\
---
type: task
domain: user documentation
default_audience: engineer
source: Grafana Writers' Toolkit task template
license: Apache-2.0
sections:
  - heading: Steps
    level: 2
    evidence:
      pattern: 'https?://'
      missing: a reference URL for the command
  - heading: Next steps
    level: 2
    optional: true
length_caps:
  engineer: 1200
  executive: 20
---
# <TASK_NAME>
"""

DOCUMENT = """\
# Install the agent

Install the agent on one host.

## Steps

Run the installer from https://example.com/agent and wait for the prompt to return.

```bash
sudo apt install agent one two three four five six seven eight nine ten
```

## Next steps

See the configuration reference.
"""


@pytest.fixture
def paths(tmp_path: Path) -> tuple[Path, Path]:
    template = tmp_path / "task.md"
    template.write_text(textwrap.dedent(TEMPLATE))
    document = tmp_path / "doc.md"
    document.write_text(DOCUMENT)
    return template, document


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args], capture_output=True, text=True, check=False
    )


def test_document_under_the_engineer_cap_passes_with_no_length_finding(paths):
    template, _ = paths
    spec = load_template(template)
    doc = parse_document(DOCUMENT)
    assert check_length(doc, spec, "engineer") == []
    assert check_length(doc, spec, "operator") == [], "no cap for the audience means no check"
    assert check_document(DOCUMENT, spec) == []
    assert check_document(DOCUMENT, spec, audience="engineer") == []


def test_executive_cap_yields_length_exceeded_naming_cap_and_count(paths):
    template, _ = paths
    spec = load_template(template)
    doc = parse_document(DOCUMENT)
    words = sum(
        len(line.split())
        for number, line in enumerate(DOCUMENT.splitlines(), start=1)
        if number not in doc.fenced_lines
    )
    assert words > 20
    findings = check_length(doc, spec, "executive")
    assert [f.code for f in findings] == ["LENGTH_EXCEEDED"]
    assert findings[0].severity == "medium"
    assert "20" in findings[0].message
    assert str(words) in findings[0].message
    assert check_document(DOCUMENT, spec, audience="executive") == findings


def test_cli_passing_document_exits_zero_with_the_json_shape(paths):
    template, document = paths
    result = _run("--template", str(template), str(document))
    assert result.returncode == 0, result.stderr
    body = json.loads(result.stdout)
    assert set(body) == {"template", "audience", "pass", "findings", "counts"}
    assert body["template"] == "task"
    assert body["audience"] == "engineer"
    assert body["pass"] is True
    assert body["findings"] == []
    assert body["counts"] == {"high": 0, "medium": 0, "low": 0, "info": 0}

    helped = _run("--help")
    assert helped.returncode == 0
    assert "usage" in helped.stdout.lower()


def test_cli_unknown_audience_exits_two_with_a_json_error_naming_it(paths):
    template, document = paths
    result = _run("--template", str(template), "--audience", "customer", str(document))
    assert result.returncode == 2
    body = json.loads(result.stdout)
    assert "customer" in body["error"]
    assert "operator" in body["error"]
    assert "Traceback" not in result.stderr


def test_cli_apparatus_errors_exit_two_and_findings_exit_one(paths, tmp_path):
    template, document = paths

    missing = _run("--template", str(template), str(tmp_path / "absent.md"))
    assert missing.returncode == 2
    assert "absent.md" in json.loads(missing.stdout)["error"]
    assert "Traceback" not in missing.stderr

    broken = tmp_path / "broken.md"
    broken.write_text(textwrap.dedent(TEMPLATE).replace("type: task\n", ""))
    bad_template = _run("--template", str(broken), str(document))
    assert bad_template.returncode == 2
    assert "type" in json.loads(bad_template.stdout)["error"]
    assert "Traceback" not in bad_template.stderr

    document.write_text(DOCUMENT.replace("https://example.com/agent ", ""))
    failing = _run("--template", str(template), str(document))
    assert failing.returncode == 1
    body = json.loads(failing.stdout)
    assert body["pass"] is False
    assert [f["code"] for f in body["findings"]] == ["EVIDENCE_MISSING"]
    assert body["counts"]["high"] == 1


def test_a_document_at_exactly_the_cap_passes_and_one_word_over_fails(tmp_path):
    doc = parse_document(DOCUMENT)
    words = sum(
        len(line.split())
        for number, line in enumerate(DOCUMENT.splitlines(), start=1)
        if number not in doc.fenced_lines
    )
    at_cap = tmp_path / "at_cap.md"
    at_cap.write_text(
        textwrap.dedent(TEMPLATE).replace("  executive: 20\n", f"  executive: {words}\n")
    )
    assert check_length(doc, load_template(at_cap), "executive") == []

    one_under = tmp_path / "one_under.md"
    one_under.write_text(
        textwrap.dedent(TEMPLATE).replace("  executive: 20\n", f"  executive: {words - 1}\n")
    )
    findings = check_length(doc, load_template(one_under), "executive")
    assert [f.code for f in findings] == ["LENGTH_EXCEEDED"]


def test_cli_non_utf8_document_or_template_exits_two_with_a_json_error(paths, tmp_path):
    template, document = paths
    latin = tmp_path / "latin.md"
    latin.write_bytes(DOCUMENT.replace("one host", "café host").encode("latin-1"))
    result = _run("--template", str(template), str(latin))
    assert result.returncode == 2, result.stderr
    body = json.loads(result.stdout)
    assert "latin.md" in body["error"]
    assert "UTF-8" in body["error"]
    assert "Traceback" not in result.stderr

    bad_template = tmp_path / "latin-template.md"
    bad_template.write_bytes(
        textwrap.dedent(TEMPLATE).replace("task template", "tâche template").encode("latin-1")
    )
    result = _run("--template", str(bad_template), str(document))
    assert result.returncode == 2, result.stderr
    body = json.loads(result.stdout)
    assert "latin-template.md" in body["error"]
    assert "UTF-8" in body["error"]
    assert "Traceback" not in result.stderr


def test_section_max_words_yields_length_exceeded_naming_the_section(tmp_path):
    """A section over its ``max_words`` for the audience is LENGTH_EXCEEDED with the
    section's heading on the finding; the words are counted outside fenced blocks, the cap is
    inclusive, and an audience the section names no cap for has no per-section check."""
    doc = parse_document(DOCUMENT)
    steps = next(h for h in doc.headings if h.text == "Steps")
    words = sum(
        len(line.split())
        for offset, line in enumerate(steps.section.split("\n"), start=1)
        if steps.line + offset not in doc.fenced_lines
    )
    assert words == 12, "the Steps prose outside the fence is one twelve-word sentence"

    def with_cap(cap: int) -> Path:
        path = tmp_path / f"cap-{cap}.md"
        path.write_text(
            textwrap.dedent(TEMPLATE).replace(
                "  - heading: Steps\n    level: 2\n",
                f"  - heading: Steps\n    level: 2\n    max_words:\n      engineer: {cap}\n",
            )
        )
        return path

    assert check_length(doc, load_template(with_cap(words)), "engineer") == []
    findings = check_length(doc, load_template(with_cap(words - 1)), "engineer")
    assert [(f.code, f.severity, f.heading, f.line) for f in findings] == [
        ("LENGTH_EXCEEDED", "medium", "Steps", steps.line)
    ]
    assert str(words) in findings[0].message and str(words - 1) in findings[0].message
    assert check_length(doc, load_template(with_cap(words - 1)), "operator") == [], (
        "no per-section cap for the audience means no per-section check"
    )
    assert check_document(DOCUMENT, load_template(with_cap(words - 1)), audience="engineer") == (
        findings
    )
