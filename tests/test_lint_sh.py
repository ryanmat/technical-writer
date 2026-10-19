# Description: Tests over scripts/lint.sh: linter detection under a controlled PATH,
# Description: the JSON report, and the exit codes for a failing tool and a missing document.
"""The script is POSIX sh and runs under /bin/sh with a PATH the test builds in tmp_path, so
the Mac and SER see the same tools: shims for the linters and symlinks to the utilities the
script itself needs. The real linters, present or not, never reach it."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
LINT_SH = ROOT / "scripts" / "lint.sh"
UTILITIES = ("awk",)
SHIM = '#!/bin/sh\necho "$0 $*"\nexit {code}\n'
REFERENCES = ROOT / "skills" / "technical-writer" / "references"


@pytest.fixture
def sandbox(tmp_path: Path) -> tuple[Path, dict[str, str]]:
    """A document, a bin directory, and an environment whose PATH holds only that directory
    and the utilities lint.sh needs."""
    tools = tmp_path / "tools"
    tools.mkdir()
    for name in UTILITIES:
        real = shutil.which(name)
        assert real is not None, f"{name} is not on the test's PATH"
        os.symlink(real, tools / name)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    doc = tmp_path / "doc.md"
    doc.write_text("# Title\n\nOne sentence.\n", encoding="utf-8")
    env = {"PATH": f"{bin_dir}:{tools}", "LC_ALL": "C"}
    return doc, env


def shim(env: dict[str, str], name: str, code: int = 0) -> Path:
    bin_dir = Path(env["PATH"].split(":")[0])
    path = bin_dir / name
    path.write_text(SHIM.format(code=code), encoding="utf-8")
    path.chmod(0o755)
    return path


def run(env: dict[str, str], *args: str) -> tuple[int, dict]:
    result = subprocess.run(
        ["/bin/sh", str(LINT_SH), *args],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.stdout.strip(), f"no stdout; stderr: {result.stderr}"
    return result.returncode, json.loads(result.stdout)


def test_neither_tool_present_exits_zero_and_points_at_the_checklist(sandbox):
    doc, env = sandbox
    code, report = run(env, str(doc))
    assert code == 0
    assert report["missing"] == ["vale", "markdownlint"]
    assert report["ran"] == []
    assert report["checklist"] is True


def test_vale_on_path_runs_with_the_skill_config_and_markdownlint_stays_missing(sandbox):
    doc, env = sandbox
    shim(env, "vale")
    code, report = run(env, str(doc))
    assert code == 0
    assert report["ran"] == ["vale"]
    assert report["missing"] == ["markdownlint"]
    output = report["results"]["vale"]["output"]
    assert str(REFERENCES / "vale" / ".vale.ini") in output, output
    assert str(doc) in output, output


def test_markdownlint_cli2_is_detected_under_the_markdownlint_name(sandbox):
    doc, env = sandbox
    shim(env, "markdownlint-cli2")
    code, report = run(env, str(doc))
    assert code == 0
    assert report["ran"] == ["markdownlint"]
    assert report["missing"] == ["vale"]
    output = report["results"]["markdownlint"]["output"]
    assert str(REFERENCES / "markdownlint.jsonc") in output, output
    assert report["results"]["markdownlint"]["exit"] == 0


def test_a_failing_tool_fails_the_script_with_its_output_captured(sandbox):
    doc, env = sandbox
    shim(env, "vale", code=1)
    shim(env, "markdownlint")
    code, report = run(env, str(doc))
    assert code == 1
    assert report["ran"] == ["vale", "markdownlint"]
    assert report["results"]["vale"]["exit"] == 1
    assert str(doc) in report["results"]["vale"]["output"]
    assert report["results"]["markdownlint"]["exit"] == 0


def test_a_missing_document_argument_exits_two_with_a_json_error(sandbox):
    _, env = sandbox
    code, report = run(env)
    assert code == 2
    assert "error" in report
    assert "document" in report["error"]
    code, report = run(env, str(Path(env["PATH"].split(":")[0]) / "absent.md"))
    assert code == 2
    assert "absent.md" in report["error"]


def test_help_exits_zero():
    result = subprocess.run(
        ["/bin/sh", str(LINT_SH), "--help"], capture_output=True, text=True, check=False
    )
    assert result.returncode == 0
    assert "lint.sh" in result.stdout


def test_vale_that_cannot_load_its_styles_is_reported_as_missing_with_the_sync_command(sandbox):
    """Review round 1: a fresh install has no synced Google package, and Vale then exits
    2 with its E201 error instead of findings. That is a linter not ready to run, never a set
    of findings: it joins the missing list with a note naming the sync command, and the script
    exits 0 as it does for any missing linter."""
    doc, env = sandbox
    bin_dir = Path(env["PATH"].split(":")[0])
    vale = bin_dir / "vale"
    vale.write_text(
        "#!/bin/sh\n"
        'printf \'{"Line": 8, "Text": "Style \\x27Google\\x27 isn\\x27t on the StylesPath", '
        '"Code": "E201"}\\n\'\n'
        "exit 2\n",
        encoding="utf-8",
    )
    vale.chmod(0o755)
    code, report = run(env, str(doc))
    assert code == 0
    assert report["ran"] == []
    assert report["missing"] == ["vale", "markdownlint"]
    assert "vale" in report["notes"]
    assert "sync" in report["notes"]["vale"]
    assert "E201" in report["notes"]["vale"]
