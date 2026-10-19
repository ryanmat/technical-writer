#!/usr/bin/env python3
# Description: Scores the hand-scored calibration set with the prose judge through the same
# Description: criteria the graders carry, writes judge.json, and compares it with scores.yaml.
"""The prose judge's calibration driver (the 2026-10-17 10:22 EDT ruling).

``evals/calibration/scores.yaml`` holds the hand score for each of six holdout outputs on
``evals/rubrics/prose.md``. ``claude plugin eval`` cannot grade a supplied document, so this
driver sends each document, with the case's template and audience, to the judge model through
``prose_judge.judge_document`` and writes ``judge.json`` beside the hand scores. Exit 0 when
every judge score is within one point of the hand score, 1 when one is not (the fix is the
rubric wording, never scores.yaml), 2 when a judge call failed or answered without a score.
"""

from __future__ import annotations

import argparse
import json
import subprocess  # noqa: F401  (the tests replace subprocess.run through this module's name)
import sys
from datetime import UTC, datetime
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import prose_judge  # noqa: E402  (a sibling module, loaded after the path insert)

CALIBRATION_DIR = HERE / "calibration"
DEFAULT_SCORES = CALIBRATION_DIR / "scores.yaml"
DEFAULT_OUT = CALIBRATION_DIR / "judge.json"
TOLERANCE = 1  # the agreement the ruling requires: within one point on every document

PASS, FAIL, APPARATUS = 0, 1, 2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="calibrate.py", description="score the calibration set with the prose judge"
    )
    parser.add_argument("--scores", default=str(DEFAULT_SCORES), help="the hand scores")
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="where judge.json lands")
    parser.add_argument(
        "--model",
        default=prose_judge.JUDGE_MODEL,
        help=f"the judge (default {prose_judge.JUDGE_MODEL})",
    )
    args = parser.parse_args(argv)
    scores_path = Path(args.scores)
    hand = yaml.safe_load(scores_path.read_text(encoding="utf-8"))
    documents = []
    try:
        for entry in hand["documents"]:
            text = (scores_path.parent / entry["file"]).read_text(encoding="utf-8")
            judgement = prose_judge.judge_document(
                text, entry["template"], entry["audience"], model=args.model
            )
            documents.append(
                {
                    "file": entry["file"],
                    "case": entry["case"],
                    "template": entry["template"],
                    "audience": entry["audience"],
                    "criteria_sha256": prose_judge.criteria_sha256(
                        entry["template"], entry["audience"]
                    ),
                    "score": judgement.score,
                    "answer": judgement.answer,
                    "cost_usd": str(judgement.cost_usd),
                }
            )
    except (prose_judge.JudgeError, OSError) as exc:
        print(json.dumps({"error": str(exc)}, indent=2))
        return APPARATUS
    result = {
        "rubric": hand["rubric"],
        "rubric_sha256": prose_judge.rubric_sha256(),
        "judge_model": args.model,
        "scored_on": datetime.now(UTC).date().isoformat(),
        "documents": documents,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    hand_scores = {entry["file"]: entry["score"] for entry in hand["documents"]}
    disagreements = 0
    for doc in documents:
        hand_score = hand_scores[doc["file"]]
        judge_score = doc["score"]
        agrees = (
            hand_score is not None
            and judge_score is not None
            and abs(judge_score - hand_score) <= TOLERANCE
        )
        disagreements += not agrees
        print(
            f"{doc['file']}: hand {hand_score}, judge "
            f"{'Unknown' if judge_score is None else judge_score}, "
            f"{'agree' if agrees else 'DISAGREE'}"
        )
    print(f"judge.json {out}")
    if disagreements:
        print(
            f"calibration: FAIL: {disagreements} disagree beyond {TOLERANCE} point; fix the rubric"
        )
        return FAIL
    print("calibration: PASS: every document within one point")
    return PASS


if __name__ == "__main__":
    sys.exit(main())
