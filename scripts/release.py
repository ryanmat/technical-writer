#!/usr/bin/env python3
# Description: Exports the tracked tree at one tag, minus the private paths, into a clone of the
# Description: public repository as one tagged commit, after scanning it for private identifiers.
"""The release export.

The build repository keeps the spec, the plan, the findings and the research; the public
repository carries everything else. One invocation reads ``git ls-tree`` at ``--tag`` in the
source repository, drops the private paths, scans every remaining text file for the private
identifiers, replaces the working tree of the public clone with the result, commits it there as
``release <tag>`` and tags the commit ``<tag>``. Nothing is rewritten: each release is one more
commit on the public branch, so the install line keeps its name and its history.

Exit codes: 0 the public commit and tag were made; 1 a private identifier is in the export (the
hits are printed, nothing is written); 2 apparatus (the tag is missing or not at the source HEAD,
a path is not a git repository, the public clone is dirty or already carries the tag, git
failed). Every outcome prints one JSON object.
"""

from __future__ import annotations

import argparse
import io
import json
import re
import subprocess
import sys
import tarfile
from pathlib import Path

# The paths the build repository keeps; a trailing slash marks a directory. The scan test in
# tests/test_public_docs.py reads the same tuple, so the tracked-tree scan and the export agree.
PRIVATE_PATHS: tuple[str, ...] = ("spec.md", "prompt_plan.md", "findings.md", "research/")

# Identifiers that name the owner, the workflow tooling or the plan artifacts, as regexes.
PRIVATE_IDENTIFIERS: tuple[str, ...] = (
    "Matuszewski",
    r"\badw\b",
    "Handoff",
    "prompt_plan",
    r"CLAUDE\.md",
    r"\.remember",
    "herdr",
)
_PRIVATE = re.compile("|".join(PRIVATE_IDENTIFIERS))

# The two files that spell the identifiers out, which every scan skips; nothing else is exempt.
SCAN_EXEMPT: tuple[str, ...] = ("scripts/release.py", "tests/test_release.py")

OK, HITS, APPARATUS = 0, 1, 2


class ReleaseError(Exception):
    """An apparatus failure; the message is the JSON error body."""


def is_private_path(name: str) -> bool:
    """True when ``name`` is one of the private paths or sits under a private directory."""
    return any(
        name == private or (private.endswith("/") and name.startswith(private))
        for private in PRIVATE_PATHS
    )


def git(cwd: Path, *args: str, binary: bool = False) -> bytes | str:
    """Run git in ``cwd`` and return stdout; a non-zero exit is a ReleaseError."""
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True)
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", "replace").strip()
        raise ReleaseError(f"git {' '.join(args)} failed in {cwd}: {detail}")
    return result.stdout if binary else result.stdout.decode("utf-8")


def repo_root(path: Path) -> Path:
    if not path.is_dir():
        raise ReleaseError(f"{path} is not a directory")
    try:
        top = git(path, "rev-parse", "--show-toplevel")
    except ReleaseError as exc:
        raise ReleaseError(f"{path} is not a git repository") from exc
    return Path(str(top).strip())


def tagged_commit(source: Path, tag: str) -> str:
    """The commit ``tag`` points at, which must be the source HEAD."""
    probe = subprocess.run(
        ["git", "rev-parse", "--verify", "-q", f"refs/tags/{tag}^{{commit}}"],
        cwd=source,
        capture_output=True,
        text=True,
    )
    if probe.returncode != 0:
        raise ReleaseError(f"tag {tag} does not exist in {source}")
    commit = probe.stdout.strip()
    head = str(git(source, "rev-parse", "HEAD")).strip()
    if commit != head:
        raise ReleaseError(
            f"tag {tag} points at {commit[:8]}, not at the source HEAD {head[:8]}; "
            "release from the tagged commit"
        )
    return commit


def export_files(source: Path, tag: str) -> list[str]:
    """Every tracked path at ``tag`` outside the private paths, in git's order."""
    listed = str(git(source, "ls-tree", "-r", "--name-only", "-z", tag))
    return [name for name in listed.split("\0") if name and not is_private_path(name)]


def read_blob(source: Path, tag: str, name: str) -> bytes:
    return git(source, "show", f"{tag}:{name}", binary=True)  # type: ignore[return-value]


def scan(source: Path, tag: str, names: list[str]) -> list[dict[str, object]]:
    """Every line of every text file in the export, the exempt two aside, that carries a private
    identifier."""
    hits: list[dict[str, object]] = []
    for name in names:
        if name in SCAN_EXEMPT:
            continue
        try:
            text = read_blob(source, tag, name).decode("utf-8")
        except UnicodeDecodeError:
            continue
        for number, line in enumerate(text.splitlines(), start=1):
            match = _PRIVATE.search(line)
            if match:
                hits.append({"path": name, "line": number, "match": match.group(0)})
    return hits


def clear_public_tree(public: Path) -> int:
    """Remove every tracked file from the public working tree; returns how many."""
    tracked = [n for n in str(git(public, "ls-files", "-z")).split("\0") if n]
    if tracked:
        git(public, "rm", "-r", "-q", "--", ".")
    return len(tracked)


def write_export(source: Path, tag: str, names: list[str], public: Path) -> None:
    """Extract the tagged files into the public tree through one git archive."""
    archive = git(source, "archive", "--format=tar", tag, "--", *names, binary=True)
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as tar:  # type: ignore[arg-type]
        for member in tar.getmembers():
            if member.name.startswith("/") or ".." in Path(member.name).parts:
                raise ReleaseError(f"archive member {member.name!r} escapes the tree")
        tar.extractall(public, filter="data")


def release(source: Path, tag: str, public: Path) -> tuple[int, dict[str, object]]:
    source = repo_root(source)
    public = repo_root(public)
    commit = tagged_commit(source, tag)
    if str(git(public, "status", "--porcelain")).strip():
        raise ReleaseError(f"the public clone {public} has uncommitted changes")
    has_tag = subprocess.run(
        ["git", "rev-parse", "--verify", "-q", f"refs/tags/{tag}"], cwd=public, capture_output=True
    )
    if has_tag.returncode == 0:
        raise ReleaseError(f"the public clone already carries the tag {tag}")
    names = export_files(source, tag)
    hits = scan(source, tag, names)
    if hits:
        return HITS, {"tag": tag, "source_commit": commit, "hits": hits}
    removed = clear_public_tree(public)
    write_export(source, tag, names, public)
    git(public, "add", "-A")
    git(public, "commit", "-q", "-m", f"release {tag}")
    git(public, "tag", tag)
    public_commit = str(git(public, "rev-parse", "HEAD")).strip()
    return OK, {
        "tag": tag,
        "source_commit": commit,
        "commit": public_commit,
        "files": len(names),
        "removed_before_export": removed,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="release.py",
        description="Export the tree at a tag, minus the private paths, to the public clone.",
    )
    parser.add_argument("--tag", required=True, help="the release tag, at the source HEAD")
    parser.add_argument(
        "--public", required=True, help="path to a clean clone of the public repository"
    )
    parser.add_argument(
        "--source", default=".", help="the source repository (default: the current directory)"
    )
    args = parser.parse_args(argv)
    try:
        code, body = release(Path(args.source), args.tag, Path(args.public))
    except ReleaseError as exc:
        print(json.dumps({"error": str(exc)}))
        return APPARATUS
    print(json.dumps(body))
    return code


if __name__ == "__main__":
    sys.exit(main())
