#!/usr/bin/env python3
# Description: The prose judge's one source: renders graders/prose-judge.md for every drafting
# Description: case from evals/rubrics/prose.md and reads the Score: line a judge answers with.
"""The prose judge.

``evals/rubrics/prose.md`` is the rubric a person and a judge model both score a document
against, 1 to 5 or Unknown. ``claude plugin eval`` reads an ``llm`` grader's criteria from the
grader file's body, so every drafting case carries ``graders/prose-judge.md`` rendered from the
rubric here, with the vote clause the CLI needs (two PASS votes of three pass the grader) and
the answer form the score reader needs (a ``Score:`` line first). ``evals/calibrate.py`` sends
the same criteria to the same judge model over the hand-scored calibration set. The CLI
records only the votes, so the gate scores each drafting run through ``judge_document`` after
the run and writes ``judge.json`` beside the result, which ``run_evals`` reads. Review cases
grade recall, not prose, and carry no judge.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "scripts"))

from check_structure import Section, TemplateSpec, templates_by_type  # noqa: E402

RUBRIC = HERE / "rubrics" / "prose.md"
CASE_ROOTS = (HERE / "holdout", HERE / "cases")
GRADER_NAME = "prose-judge"
SIDECAR = "judge.json"  # written beside a result's run.json: one judge score per drafting run
JUDGE_MODEL = "claude-sonnet-5-5"  # the one judge for the gate and the calibration set
PASS_SCORE = 3  # the vote clause: a run below this fails the grader (the spec's floor)

SCORE_LINE = re.compile(r"^\s*Score:\s*(Unknown|[1-5])\b", re.IGNORECASE | re.MULTILINE)
ANY_SCORE_LINE = re.compile(r"^\s*Score:", re.IGNORECASE | re.MULTILINE)

VOTE_CLAUSE = f"""\
## How to vote

Begin your answer with one line, `Score: N` with N from 1 to 5, or `Score: Unknown`, then the
evidence sentences the rubric asks for.

PASS if the score is {PASS_SCORE} or more.
FAIL if the score is below {PASS_SCORE}, or if the answer is Unknown.
"""

VERIFIES = (
    "Verifies: the prose of the final document against evals/rubrics/prose.md (leads with the "
    "point, one idea per paragraph, no filler, register fits the audience), scored 1 to 5 by "
    f"the judge model; the run passes this grader at {PASS_SCORE} or more, and run_evals reads "
    "the score for the median rule.\n"
    "Cannot verify: structure, evidence slots, length and banned words; check_structure.py "
    "owns those, and a marker's presence is the marker grader's."
)


JUDGE_BUDGET_USD = "0.50"  # the ceiling on one judge call; a stripped call costs about a cent
SYSTEM_PROMPT = (
    "You are the prose judge for a technical writing plugin. Score the document under the "
    "heading 'The document to score' against the rubric above it, as a reader of the named "
    "audience would receive it. Answer exactly as the section 'How to vote' says, nothing else."
)
DOCUMENT_HEADING = "## The document to score\n\n"


_BODY_HEADING = re.compile(r"^#{2,6}[ \t]+(.*?)[ \t]*$", re.MULTILINE)
_SECTION_OPENER = re.compile(r"^(?:Required|Optional)\.\s*")  # a comma opener is a clause and stays
SECTIONS_HEADING = "## The template's sections"


class JudgeError(ValueError):
    """A judge answer the score reader cannot use: no Score: line, or one outside the scale;
    a judge call that did not complete; or a document whose type names no template."""


@dataclass(frozen=True)
class Judgement:
    score: int | None  # None is Unknown
    answer: str
    cost_usd: Decimal


def template_spec(template: str) -> TemplateSpec:
    """The shipped template whose ``type`` is ``template``; a type naming none is a JudgeError,
    since every case's expected.json and every calibration entry names a shipped one."""
    specs = templates_by_type()
    if template not in specs:
        raise JudgeError(f"the document's type {template!r} names no template")
    return specs[template]


def _first_paragraphs(body: str) -> dict[str, str]:
    """The first paragraph under each heading of a template body, by heading text."""
    found: dict[str, str] = {}
    matches = list(_BODY_HEADING.finditer(body))
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        paragraph = body[match.end() : end].strip().split("\n\n", 1)[0]
        found[match.group(1)] = " ".join(paragraph.split()).rstrip(":")
    return found


def section_guide(spec: TemplateSpec) -> str:
    """One line per template section, in order: its label, ``(optional)`` when it is, and
    the template body's first paragraph under the heading of that name with its one-word
    Required or Optional opener and any trailing colon dropped; a section whose heading the
    body never uses carries its label alone. This is what lets the judge tell a section doing
    its job from filler."""
    paragraphs = _first_paragraphs(spec.body)
    lines = []
    for section in spec.sections:
        label = section.label + (" (optional)" if section.optional else "")
        purpose = _SECTION_OPENER.sub("", paragraphs.get(_heading_key(section), ""))
        lines.append(f"- {label}: {purpose}" if purpose else f"- {label}")
    return "\n".join(lines)


def _heading_key(section: Section) -> str:
    return section.heading if section.heading is not None else section.label


def criteria(template: str, audience: str) -> str:
    """The text the judge reads: the rubric file verbatim, the document's template type and
    audience, the template's sections with what each asks for (the facts the rubric says the
    judge is given), then the vote clause."""
    rubric = RUBRIC.read_text(encoding="utf-8").rstrip("\n")
    spec = template_spec(template)
    article = "An" if template[:1].lower() in "aeiou" else "A"
    given = f"## The document\n\n{article} {template} written for the {audience} audience.\n"
    sections = (
        f"{SECTIONS_HEADING}\n\nIn the template's order, each with what the template asks of it; "
        "the No filler criterion says how a section's job bears on a repeated fact.\n\n"
        + section_guide(spec)
        + "\n"
    )
    return rubric + "\n\n" + given + "\n" + sections + "\n" + VOTE_CLAUSE


def case_expected(case: Path) -> dict:
    return json.loads((case / "expected.json").read_text(encoding="utf-8"))


def render_grader(case: Path) -> str:
    """The grader file for one drafting case, byte for byte, from its expected.json."""
    expected = case_expected(case)
    front = "---\ntype: llm\nfocus: last_message\nweight: 1\n---\n\n"
    return front + VERIFIES + "\n\n" + criteria(expected["template"], expected["audience"])


def drafting_cases() -> list[Path]:
    """Every case under the eval roots whose expected.json mode is not review."""
    found: list[Path] = []
    for root in CASE_ROOTS:
        for case in sorted(p for p in root.iterdir() if p.is_dir()):
            if case_expected(case).get("mode", "write") != "review":
                found.append(case)
    return found


def parse_score(answer: str) -> int | None:
    """The score on the judge's ``Score:`` line, 1 to 5, or None for Unknown."""
    match = SCORE_LINE.search(answer)
    if match is None:
        if ANY_SCORE_LINE.search(answer):
            raise JudgeError(f"the judge's Score: line is not 1 to 5 or Unknown: {answer[:120]!r}")
        raise JudgeError(f"the judge answered without a Score: line: {answer[:120]!r}")
    value = match.group(1)
    return None if value.lower() == "unknown" else int(value)


def judge_argv(model: str, budget_usd: str = JUDGE_BUDGET_USD) -> list[str]:
    """A context-free `claude -p`: no tools, no MCP servers, no settings and so no plugins or
    hooks, one fixed system prompt, a budget ceiling. The prompt arrives on stdin."""
    return [
        "claude",
        "-p",
        "--model",
        model,
        "--output-format",
        "json",
        "--no-session-persistence",
        "--tools",
        "",
        "--strict-mcp-config",
        "--setting-sources",
        "",
        "--max-budget-usd",
        budget_usd,
        "--system-prompt",
        SYSTEM_PROMPT,
    ]


def judge_document(text: str, template: str, audience: str, model: str = JUDGE_MODEL) -> Judgement:
    """Score one document: the grader's criteria, then the document, to the judge model."""
    prompt = criteria(template, audience) + "\n" + DOCUMENT_HEADING + text.rstrip("\n") + "\n"
    argv = judge_argv(model)
    with tempfile.TemporaryDirectory(prefix="prose-judge-") as cwd:  # no project files to load
        try:
            proc = subprocess.run(
                argv, input=prompt, capture_output=True, text=True, cwd=cwd, check=False
            )
        except OSError as exc:
            raise JudgeError(f"claude is not available to judge: {exc}") from exc
    if proc.returncode != 0:
        raise JudgeError(
            f"the judge call exited {proc.returncode}: {(proc.stderr or proc.stdout).strip()[:400]}"
        )
    try:
        data = json.loads(proc.stdout)
    except ValueError as exc:
        raise JudgeError(f"the judge call printed no JSON result: {proc.stdout[:200]!r}") from exc
    if (
        not isinstance(data, dict)
        or data.get("is_error")
        or not isinstance(data.get("result"), str)
    ):
        raise JudgeError(f"the judge call did not succeed: {json.dumps(data)[:400]}")
    answer = data["result"]
    return Judgement(
        score=parse_score(answer),
        answer=answer,
        cost_usd=Decimal(str(data.get("total_cost_usd", "0"))),
    )


def rubric_sha256() -> str:
    return hashlib.sha256(RUBRIC.read_bytes()).hexdigest()


def criteria_sha256(template: str, audience: str) -> str:
    """The hash of the full criteria text a document of this type and audience is judged
    against: the rubric and the template's section guide together, so a template body edit
    changes it as a rubric edit does."""
    return hashlib.sha256(criteria(template, audience).encode("utf-8")).hexdigest()


def write_sidecar(result_dir: Path, model: str, runs: list[dict]) -> Path:
    """Write ``judge.json`` beside a result: the judge model, the rubric's hash, and one entry
    per judged run (``case``, ``run``, ``score``, ``answer``, ``cost_usd``)."""
    path = Path(result_dir) / SIDECAR
    body = {"judge_model": model, "rubric_sha256": rubric_sha256(), "runs": runs}
    path.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
    return path


def read_sidecar(result_dir: Path) -> dict[tuple[str, int], dict]:
    """The sidecar's entries keyed by (case, run), or an empty mapping when there is none."""
    path = Path(result_dir) / SIDECAR
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise JudgeError(f"{path} is not JSON: {exc}") from exc
    return {(entry["case"], int(entry["run"])): entry for entry in data.get("runs", [])}


def write_graders() -> list[Path]:
    """Write graders/prose-judge.md into every drafting case; the paths written."""
    written = []
    for case in drafting_cases():
        path = case / "graders" / f"{GRADER_NAME}.md"
        path.write_text(render_grader(case), encoding="utf-8")
        written.append(path)
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="prose_judge.py",
        description="render graders/prose-judge.md into every drafting case from the rubric",
    )
    parser.parse_args(argv)
    for path in write_graders():
        print(path.relative_to(ROOT).as_posix())
    return 0


if __name__ == "__main__":
    sys.exit(main())
