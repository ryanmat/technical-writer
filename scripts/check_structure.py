# Description: Structural checker shared by the technical-writer skill and its eval
# Description: graders. Loads template front matter into a TemplateSpec and checks documents.
"""Template front matter schema, loader, and structural checks for the technical-writer plugin.

Every template under ``skills/technical-writer/references/templates/`` is a Markdown
file whose YAML front matter is the single source of truth for both the skill (what to
write) and the grader (what to check). This module reads that front matter, parses a
document's headings, and reports findings against the template.

Schema, with one complete example. Keys outside this schema are rejected at every level,
so a misspelled key cannot silently disable a check::

    ---
    type: task                      # required; the document type the template covers
    domain: user documentation      # required; one of DOMAINS
    default_audience: engineer      # required; one of AUDIENCES
    source: Grafana Writers' Toolkit task template   # required; the standard it follows
    license: Apache-2.0             # required; the source's license, for attribution.md
    procedure: true                 # optional, default false; the procedure rules apply
    procedure_section: Steps        # required when procedure is true; a section's label (its
                                    # heading, its label key, or its heading_pattern's text);
                                    # the rules apply to every heading that section matches
    summary_required: true          # optional, default true; a summary line must follow the H1
    h1_pattern: '^[A-Z]'            # optional regex the single H1 must match
    sections:                       # required, non-empty, in the order the document keeps
      - heading: Before you begin   # exactly one of heading / heading_pattern
        level: 2                    # required, 1 to 6
        optional: true              # optional, default false
      - heading: Steps
        level: 2
        evidence:                   # optional; the slot this section must fill
          pattern: 'https?://'      # regex that proves the slot is filled
          missing: a reference URL for the command   # what the [UNVERIFIED: ...] marker names
        max_words:                  # optional; words for this section alone, keyed by audience
          regulator: 100
      - heading_pattern: '^(Next steps|What next)$'
        label: the next steps section  # optional; names a pattern section in findings
        level: 2
        optional: true
    length_caps:                    # optional; words, keyed by audience
      engineer: 1200
      operator: 800
    banned_patterns:                # optional; beyond the global set in style-rules.md
      - pattern: '\\u2014'
        rule: no em dashes
    ---
    # <TASK_NAME>

Every validation failure raises :class:`TemplateError` and names the file path.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from itertools import pairwise
from pathlib import Path
from typing import Any

import yaml

AUDIENCES: tuple[str, ...] = (
    "engineer",
    "operator",
    "executive",
    "regulator",
    "auditor",
    "data subject",
    "downstream provider",
)

DOMAINS: tuple[str, ...] = (
    "user documentation",
    "engineering",
    "API",
    "AI governance",
    "security",
    "privacy",
)

FRONT_MATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?(.*)\Z", re.DOTALL)
_HEADING = re.compile(r"^(#{1,6})[ \t]+(.*?)(?:[ \t]+#+)?[ \t]*$")
_FENCE = re.compile(r"^[ ]{0,3}(`{3,}|~{3,})")

_TOP_KEYS = frozenset(
    {
        "type",
        "domain",
        "default_audience",
        "source",
        "license",
        "procedure",
        "procedure_section",
        "summary_required",
        "h1_pattern",
        "sections",
        "length_caps",
        "banned_patterns",
    }
)
_SECTION_KEYS = frozenset(
    {"heading", "heading_pattern", "label", "level", "optional", "evidence", "max_words"}
)
_EVIDENCE_KEYS = frozenset({"pattern", "missing"})
_BANNED_KEYS = frozenset({"pattern", "rule"})


class TemplateError(ValueError):
    """A template's front matter is missing, malformed, or fails validation."""


@dataclass(frozen=True)
class Evidence:
    pattern: re.Pattern[str]
    missing: str


@dataclass(frozen=True)
class BannedPattern:
    pattern: re.Pattern[str]
    rule: str


@dataclass(frozen=True)
class Section:
    """One template section. ``label`` names it in findings: the template's ``label`` key
    when it has one, else the heading text, else the pattern source."""

    level: int
    heading: str | None = None
    heading_pattern: re.Pattern[str] | None = None
    optional: bool = False
    evidence: Evidence | None = None
    label: str = ""
    max_words: dict[str, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.label:
            fallback = self.heading if self.heading is not None else self.heading_pattern.pattern
            object.__setattr__(self, "label", fallback)


@dataclass(frozen=True)
class TemplateSpec:
    path: Path
    type: str
    domain: str
    default_audience: str
    source: str
    license: str
    sections: tuple[Section, ...]
    procedure: bool = False
    procedure_section: str | None = None
    summary_required: bool = True
    h1_pattern: re.Pattern[str] | None = None
    length_caps: dict[str, int] = field(default_factory=dict)
    banned_patterns: tuple[BannedPattern, ...] = ()
    body: str = ""


_REFERENCES = Path(__file__).resolve().parent.parent / "skills" / "technical-writer" / "references"
TEMPLATES_DIR = _REFERENCES / "templates"


def templates_by_type(directory: str | Path = TEMPLATES_DIR) -> dict[str, TemplateSpec]:
    """Every template under ``directory`` keyed by its ``type``, the lookup the eval grader
    and the prose judge share."""
    specs: dict[str, TemplateSpec] = {}
    for template in sorted(Path(directory).glob("*.md")):
        spec = load_template(template)
        specs[spec.type] = spec
    return specs


def load_template(path: str | Path) -> TemplateSpec:
    """Split the template at ``path`` into front matter and body and validate the schema."""
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise TemplateError(f"{path}: not UTF-8 text ({exc.reason} at byte {exc.start})") from exc
    match = FRONT_MATTER.match(text)
    if match is None:
        raise TemplateError(f"{path}: no YAML front matter block (--- ... ---) at the top")
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        raise TemplateError(f"{path}: front matter is not valid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise TemplateError(f"{path}: front matter must be a mapping, got {type(data).__name__}")
    loader = _Loader(path, data)
    return loader.build(match.group(2))


class _Loader:
    """Field-by-field validation of one template's front matter mapping."""

    def __init__(self, path: Path, data: dict[str, Any]) -> None:
        self.path = path
        self.data = data

    def fail(self, message: str) -> TemplateError:
        return TemplateError(f"{self.path}: {message}")

    def known_keys(self, mapping: dict[str, Any], allowed: frozenset[str], *, where: str) -> None:
        unknown = sorted(str(key) for key in mapping if key not in allowed)
        if unknown:
            raise self.fail(
                f"{where}: unknown key {unknown[0]!r}; known keys are {', '.join(sorted(allowed))}"
            )

    def build(self, body: str) -> TemplateSpec:
        self.known_keys(self.data, _TOP_KEYS, where="front matter")
        procedure = self.bool("procedure", default=False)
        procedure_section = self.optional_str("procedure_section")
        if procedure and procedure_section is None:
            raise self.fail("'procedure' is true but 'procedure_section' names no heading")
        default_audience = self.required_str("default_audience")
        if default_audience not in AUDIENCES:
            raise self.fail(
                f"'default_audience' is {default_audience!r}; audiences are {_audience_list()}"
            )
        domain = self.required_str("domain")
        if domain not in DOMAINS:
            raise self.fail(f"'domain' is {domain!r}; domains are {', '.join(DOMAINS)}")
        sections = self.sections()
        declared = [section.label for section in sections]
        if procedure_section is not None and procedure_section not in declared:
            raise self.fail(
                f"'procedure_section' is {procedure_section!r}, which names no section label "
                f"in 'sections' ({', '.join(declared)})"
            )
        return TemplateSpec(
            path=self.path,
            type=self.required_str("type"),
            domain=domain,
            default_audience=default_audience,
            source=self.required_str("source"),
            license=self.required_str("license"),
            sections=sections,
            procedure=procedure,
            procedure_section=procedure_section,
            summary_required=self.bool("summary_required", default=True),
            h1_pattern=self.optional_regex("h1_pattern", where="'h1_pattern'"),
            length_caps=self.length_caps(),
            banned_patterns=self.banned_patterns(),
            body=body,
        )

    def required_str(self, key: str) -> str:
        value = self.data.get(key)
        if not isinstance(value, str) or not value.strip():
            raise self.fail(f"'{key}' is required and must be a non-empty string")
        return value

    def optional_str(self, key: str) -> str | None:
        value = self.data.get(key)
        if value is None:
            return None
        if not isinstance(value, str) or not value.strip():
            raise self.fail(f"'{key}' must be a non-empty string when present")
        return value

    def bool(self, key: str, *, default: bool) -> bool:
        value = self.data.get(key, default)
        if not isinstance(value, bool):
            raise self.fail(f"'{key}' must be true or false, got {value!r}")
        return value

    def optional_regex(self, key: str, *, where: str) -> re.Pattern[str] | None:
        value = self.data.get(key)
        if value is None:
            return None
        return self.compile(value, where=where)

    def compile(self, value: Any, *, where: str) -> re.Pattern[str]:
        if not isinstance(value, str) or not value:
            raise self.fail(f"{where}: pattern must be a non-empty string, got {value!r}")
        try:
            return re.compile(value)
        except re.error as exc:
            raise self.fail(f"{where}: invalid regex {value!r}: {exc}") from exc

    def sections(self) -> tuple[Section, ...]:
        raw = self.data.get("sections")
        if not isinstance(raw, list) or not raw:
            raise self.fail("'sections' is required and must be a non-empty list")
        sections: list[Section] = []
        seen: set[tuple[str, int]] = set()
        for index, item in enumerate(raw):
            where = f"sections[{index}]"
            if not isinstance(item, dict):
                raise self.fail(f"{where}: each section must be a mapping")
            self.known_keys(item, _SECTION_KEYS, where=where)
            heading = item.get("heading")
            heading_pattern = item.get("heading_pattern")
            if (heading is None) == (heading_pattern is None):
                raise self.fail(
                    f"{where}: exactly one of 'heading' or 'heading_pattern' is required"
                )
            if heading is not None and (not isinstance(heading, str) or not heading.strip()):
                raise self.fail(f"{where}: 'heading' must be a non-empty string")
            level = item.get("level")
            if not isinstance(level, int) or isinstance(level, bool) or not 1 <= level <= 6:
                raise self.fail(f"{where}: 'level' is required and must be an integer from 1 to 6")
            label = heading if heading is not None else str(heading_pattern)
            where = f"section {label!r}"
            compiled_pattern = (
                self.compile(heading_pattern, where=f"{where} heading_pattern")
                if heading_pattern is not None
                else None
            )
            optional = item.get("optional", False)
            if not isinstance(optional, bool):
                raise self.fail(f"{where}: 'optional' must be true or false")
            custom_label = item.get("label")
            if custom_label is not None and (
                not isinstance(custom_label, str) or not custom_label.strip()
            ):
                raise self.fail(f"{where}: 'label' must be a non-empty string")
            for name in {label, custom_label or label}:
                key = (name, level)
                if key in seen:
                    raise self.fail(
                        f"{where} appears twice at level {level}: headings and labels must be "
                        f"unique ({name!r})"
                    )
                seen.add(key)
            sections.append(
                Section(
                    level=level,
                    heading=heading,
                    heading_pattern=compiled_pattern,
                    optional=optional,
                    evidence=self.evidence(item.get("evidence"), where=where),
                    label=custom_label or "",
                    max_words=self.word_caps(item.get("max_words"), where=f"{where} max_words"),
                )
            )
        return tuple(sections)

    def evidence(self, raw: Any, *, where: str) -> Evidence | None:
        if raw is None:
            return None
        if not isinstance(raw, dict):
            raise self.fail(f"{where}: 'evidence' must be a mapping of 'pattern' and 'missing'")
        self.known_keys(raw, _EVIDENCE_KEYS, where=f"{where} evidence")
        missing = raw.get("missing")
        if not isinstance(missing, str) or not missing.strip():
            raise self.fail(f"{where}: evidence 'missing' must name what the slot needs")
        return Evidence(
            pattern=self.compile(raw.get("pattern"), where=f"{where} evidence"), missing=missing
        )

    def length_caps(self) -> dict[str, int]:
        return self.word_caps(self.data.get("length_caps"), where="'length_caps'")

    def word_caps(self, raw: Any, *, where: str) -> dict[str, int]:
        """Words keyed by audience: the document's ``length_caps`` or a section's
        ``max_words``, both the same shape."""
        if raw is None:
            return {}
        if not isinstance(raw, dict):
            raise self.fail(f"{where} must be a mapping of audience to word count")
        caps: dict[str, int] = {}
        for audience, words in raw.items():
            if audience not in AUDIENCES:
                raise self.fail(
                    f"{where} names unknown audience {audience!r}; audiences are {_audience_list()}"
                )
            if not isinstance(words, int) or isinstance(words, bool) or words <= 0:
                raise self.fail(f"{where} for {audience!r} must be a positive word count")
            caps[audience] = words
        return caps

    def banned_patterns(self) -> tuple[BannedPattern, ...]:
        raw = self.data.get("banned_patterns")
        if raw is None:
            return ()
        if not isinstance(raw, list):
            raise self.fail("'banned_patterns' must be a list of 'pattern' and 'rule' pairs")
        banned: list[BannedPattern] = []
        for index, item in enumerate(raw):
            where = f"banned_patterns[{index}]"
            if not isinstance(item, dict):
                raise self.fail(f"{where}: each entry must be a mapping of 'pattern' and 'rule'")
            self.known_keys(item, _BANNED_KEYS, where=where)
            rule = item.get("rule")
            if not isinstance(rule, str) or not rule.strip():
                raise self.fail(f"{where}: 'rule' must name the prose rule the pattern enforces")
            pattern = self.compile(item.get("pattern"), where=where)
            banned.append(BannedPattern(pattern=pattern, rule=rule))
        return tuple(banned)


def _audience_list() -> str:
    return ", ".join(AUDIENCES)


@dataclass(frozen=True)
class Finding:
    """One structural or prose finding against a document.

    ``line`` is 1-based and ``None`` when the finding has no location, as for a section
    the document never opens. ``rule`` is the plain-words name of the rule broken.
    """

    code: str
    severity: str
    line: int | None
    heading: str | None
    rule: str
    message: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "severity": self.severity,
            "line": self.line,
            "heading": self.heading,
            "rule": self.rule,
            "message": self.message,
        }


@dataclass(frozen=True)
class Heading:
    """An ATX heading outside any fenced block, with the text that follows it.

    ``body`` runs to the line before the next heading of any level: the text directly
    under this heading. ``section`` runs to the line before the next heading at the same
    or a shallower level, so it includes every subheading the author adds beneath it.
    """

    level: int
    text: str
    line: int
    body: str
    section: str


@dataclass(frozen=True)
class Document:
    """A parsed Markdown document: its lines and its headings in file order."""

    text: str
    headings: tuple[Heading, ...]
    fenced_lines: frozenset[int]

    @property
    def lines(self) -> list[str]:
        return self.text.splitlines()


def parse_document(text: str) -> Document:
    """Collect the ATX headings of ``text``, skipping fenced code blocks.

    A fence opens on three or more backticks or tildes (any info string) and closes on a
    fence of the same character at least as long, per CommonMark. Lines inside it are never
    headings. Each heading's body runs to the line before the next heading, and its
    section to the line before the next heading at the same or a shallower level.
    """
    lines = text.splitlines()
    found: list[tuple[int, str, int]] = []
    fenced: set[int] = set()
    fence: tuple[str, int] | None = None
    for number, line in enumerate(lines, start=1):
        fence_match = _FENCE.match(line)
        if fence is not None:
            fenced.add(number)
            if (
                fence_match is not None
                and fence_match.group(1)[0] == fence[0]
                and len(fence_match.group(1)) >= fence[1]
                and not line.strip().strip(fence[0])
            ):
                fence = None
            continue
        if fence_match is not None:
            fence = (fence_match.group(1)[0], len(fence_match.group(1)))
            fenced.add(number)
            continue
        heading_match = _HEADING.match(line)
        if heading_match is not None:
            found.append((len(heading_match.group(1)), heading_match.group(2).strip(), number))
    headings: list[Heading] = []
    for index, (level, heading_text, number) in enumerate(found):
        end = found[index + 1][2] - 1 if index + 1 < len(found) else len(lines)
        section_end = next(
            (later[2] - 1 for later in found[index + 1 :] if later[0] <= level), len(lines)
        )
        headings.append(
            Heading(
                level=level,
                text=heading_text,
                line=number,
                body="\n".join(lines[number:end]),
                section="\n".join(lines[number:section_end]),
            )
        )
    return Document(text=text, headings=tuple(headings), fenced_lines=frozenset(fenced))


def check_sections(doc: Document, spec: TemplateSpec) -> list[Finding]:
    """Check the document's headings against the template's sections.

    Every required section must appear; required sections present must keep the template's
    order; a heading at a level the template declares that matches no section is unknown;
    exactly one H1 is required when the template wants a summary line or an H1 pattern; and
    that one H1 must match the template's ``h1_pattern`` when it has one. Headings deeper
    than the template's deepest declared level are the author's to use.
    """
    findings: list[Finding] = []
    declared_levels = {section.level for section in spec.sections}
    deepest = max(declared_levels)
    first_match: dict[int, Heading] = {}
    for heading in doc.headings:
        if heading.level == 1 and 1 not in declared_levels:
            continue
        index = _match_section(heading, spec)
        if index is None:
            if heading.level <= deepest:
                findings.append(
                    Finding(
                        code="SECTION_UNKNOWN",
                        severity="medium",
                        line=heading.line,
                        heading=heading.text,
                        rule="heading listed in template",
                        message=(
                            f"line {heading.line}: heading {heading.text!r} is not a section "
                            f"of the {spec.type} template"
                        ),
                    )
                )
            continue
        first_match.setdefault(index, heading)
    for index, section in enumerate(spec.sections):
        if section.optional or index in first_match:
            continue
        findings.append(
            Finding(
                code="SECTION_MISSING",
                severity="high",
                line=None,
                heading=section.label,
                rule="required section present",
                message=f"required section {section.label!r} is missing",
            )
        )
    present = sorted(
        (
            (heading.line, index)
            for index, heading in first_match.items()
            if not spec.sections[index].optional
        ),
    )
    for (_, earlier), (_, later) in pairwise(present):
        if earlier > later:
            before, after = spec.sections[later], spec.sections[earlier]
            findings.append(
                Finding(
                    code="SECTION_ORDER",
                    severity="medium",
                    line=first_match[later].line,
                    heading=before.label,
                    rule="sections in template order",
                    message=(
                        f"section {before.label!r} comes after {after.label!r}; "
                        f"the template puts {before.label!r} first"
                    ),
                )
            )
    if spec.summary_required or spec.h1_pattern is not None:
        titles = [heading for heading in doc.headings if heading.level == 1]
        if len(titles) != 1:
            findings.append(
                Finding(
                    code="H1_COUNT",
                    severity="medium",
                    line=titles[0].line if titles else None,
                    heading=None,
                    rule="one H1 title",
                    message=f"found {len(titles)} H1 headings; exactly one is required",
                )
            )
        elif spec.h1_pattern is not None and not spec.h1_pattern.search(titles[0].text):
            findings.append(
                Finding(
                    code="H1_PATTERN",
                    severity="medium",
                    line=titles[0].line,
                    heading=titles[0].text,
                    rule="title in the template's form",
                    message=(
                        f"line {titles[0].line}: title {titles[0].text!r} does not match the "
                        f"{spec.type} template's title pattern {spec.h1_pattern.pattern!r}"
                    ),
                )
            )
    return findings


def _match_section(heading: Heading, spec: TemplateSpec) -> int | None:
    """The index of the first template section the heading satisfies, or None."""
    for index, section in enumerate(spec.sections):
        if section.level != heading.level:
            continue
        if section.heading is not None and section.heading == heading.text:
            return index
        if section.heading_pattern is not None and section.heading_pattern.search(heading.text):
            return index
    return None


UNVERIFIED = re.compile(r"\[UNVERIFIED:[^\]]*\]")
_INLINE_CODE = re.compile(r"(`+)(?:(?!\1).)+\1")
_LINK_DESTINATION = re.compile(r"\]\([^)]*\)")
_BARE_URL = re.compile(r"https?://\S+")
_NOT_PROSE = (_INLINE_CODE, _LINK_DESTINATION, _BARE_URL)
_SENTENCE_END = re.compile(r"[.!?](?:\s|$)")

# One rule set for every type (spec R5), each entry (pattern, rule, source). The words now
# and new stay out: their ordinary uses outnumber the timeless-breaking one, so the by-hand
# checklist carries them instead.
GLOBAL_BANS: tuple[tuple[str, str, str], ...] = (
    ("\u2014", "no em dashes", "spec R5; house rule; Splunk Vale ruleset, Dashes.yml"),
    ("\u2013", "no en dashes", "spec R5; house rule; Splunk Vale ruleset, Dashes.yml"),
    (
        r"(?i)\b(?:we recommend|it is recommended)\b",
        "state the requirement and the reason, do not recommend",
        "spec R5; Grafana Writers' Toolkit, Style conventions",
    ),
    (
        r"(?i)\brefer to\b",
        "write see for cross-references",
        "spec R5; Grafana Writers' Toolkit, Word list",
    ),
    (
        r"(?i)\b(?:easy|easily|simple|simply|quickly)\b",
        "no subjective words",
        "spec R5; Google developer documentation style guide, Word list",
    ),
    (
        r"(?i)\b(?:currently|soon)\b",
        "no timeless-breaking words outside dated content",
        "spec R5; Google developer documentation style guide, Timeless documentation",
    ),
)
_GLOBAL_BANS_COMPILED: tuple[tuple[re.Pattern[str], str], ...] = tuple(
    (re.compile(pattern), rule) for pattern, rule, _ in GLOBAL_BANS
)


def check_evidence(doc: Document, spec: TemplateSpec) -> list[Finding]:
    """List every ``[UNVERIFIED: ...]`` marker at info, and check that every section with an
    evidence slot fills it or marks it.

    Every marker outside fenced code is a finding, wherever it sits: the document's owner
    reads the list to know what to fill, and a marker that names the missing fact in the
    slot's own words is listed like any other. The slot is searched across the whole section,
    subheadings included; a marker in the section's prose stands in for the slot, and one
    inside fenced code is not prose and stands in for nothing. A section the document never
    opens is SECTION_MISSING's to report, not this check's.
    """
    findings: list[Finding] = []
    enclosing: str | None = None
    headings_by_line = {heading.line: heading.text for heading in doc.headings}
    for number, line in enumerate(doc.lines, start=1):
        enclosing = headings_by_line.get(number, enclosing)
        if number in doc.fenced_lines:
            continue
        for marker in UNVERIFIED.finditer(line):
            findings.append(
                Finding(
                    code="EVIDENCE_UNVERIFIED",
                    severity="info",
                    line=number,
                    heading=enclosing,
                    rule="evidence slot filled or marked",
                    message=f"{marker.group(0)} awaits its owner",
                )
            )
    first_match: dict[int, Heading] = {}
    for heading in doc.headings:
        index = _match_section(heading, spec)
        if index is not None:
            first_match.setdefault(index, heading)
    for index, section in enumerate(spec.sections):
        if section.evidence is None or index not in first_match:
            continue
        heading = first_match[index]
        if section.evidence.pattern.search(heading.section):
            continue
        if UNVERIFIED.search(_prose_lines(doc, heading)):
            continue  # listed above; the marker stands in for the slot
        findings.append(
            Finding(
                code="EVIDENCE_MISSING",
                severity="high",
                line=heading.line,
                heading=heading.text,
                rule="evidence slot filled or marked",
                message=(
                    f"section {heading.text!r} lacks {section.evidence.missing}; fill it or "
                    f"write [UNVERIFIED: {section.evidence.missing}]"
                ),
            )
        )
    return findings


def _prose_lines(doc: Document, heading: Heading) -> str:
    """The heading's section with its fenced lines blanked, each kept as an empty line."""
    lines = heading.section.split("\n")
    return "\n".join(
        "" if heading.line + offset in doc.fenced_lines else line
        for offset, line in enumerate(lines, start=1)
    )


def check_bans(doc: Document, spec: TemplateSpec) -> list[Finding]:
    """Report every banned pattern, global and template-specific, in prose.

    Prose is every line outside a fenced block with its inline code spans, link
    destinations, and bare URLs blanked out.
    """
    patterns = list(_GLOBAL_BANS_COMPILED) + [
        (banned.pattern, banned.rule) for banned in spec.banned_patterns
    ]
    findings: list[Finding] = []
    for number, line in enumerate(doc.lines, start=1):
        if number in doc.fenced_lines:
            continue
        prose = _blank_non_prose(line)
        for pattern, rule in patterns:
            for match in pattern.finditer(prose):
                findings.append(
                    Finding(
                        code="BANNED_PATTERN",
                        severity="low",
                        line=number,
                        heading=None,
                        rule=rule,
                        message=f"line {number}: {match.group(0)!r} breaks the rule: {rule}",
                    )
                )
    return findings


def _blank_non_prose(line: str) -> str:
    """Replace inline code, link destinations, and bare URLs with spaces of the same width."""
    for pattern in _NOT_PROSE:
        line = pattern.sub(lambda m: " " * len(m.group(0)), line)
    return line


def check_summary(doc: Document, spec: TemplateSpec) -> list[Finding]:
    """Require exactly one sentence in the first paragraph under the H1.

    A document with no single H1 is H1_COUNT's to report, so this check stays silent there.
    """
    if not spec.summary_required:
        return []
    titles = [heading for heading in doc.headings if heading.level == 1]
    if len(titles) != 1:
        return []
    title = titles[0]
    body_lines = title.body.split("\n")
    start = next((i for i, line in enumerate(body_lines) if line.strip()), None)
    if start is None:
        return [
            Finding(
                code="SUMMARY_MISSING",
                severity="medium",
                line=title.line,
                heading=title.text,
                rule="one-sentence summary under the title",
                message="no summary line follows the title; write one sentence before the "
                "first section",
            )
        ]
    end = next((i for i in range(start, len(body_lines)) if not body_lines[i].strip()), None)
    paragraph = " ".join(body_lines[start:end]).strip()
    prose = _INLINE_CODE.sub(" ", paragraph)
    sentences = len(_SENTENCE_END.findall(prose))
    if sentences == 1:
        return []
    return [
        Finding(
            code="SUMMARY_MISSING",
            severity="medium",
            line=title.line + start + 1,
            heading=title.text,
            rule="one-sentence summary under the title",
            message=f"the line under the title has {sentences} sentences; write exactly one",
        )
    ]


def passes(findings: list[Finding]) -> bool:
    """A document passes when no finding is high, medium, or low."""
    return not any(finding.severity in {"high", "medium", "low"} for finding in findings)


SEVERITIES: tuple[str, ...] = ("high", "medium", "low", "info")


def check_length(doc: Document, spec: TemplateSpec, audience: str) -> list[Finding]:
    """Count words outside fenced blocks against the template's cap for the audience, then
    each section's words against its own ``max_words`` cap for the audience.

    An audience with no cap in the template has no document length check, and a section
    with no ``max_words`` for the audience has no per-section check. A section's words are
    counted over its whole span, subheadings included, from the first heading that matches
    it, as the evidence check reads it.
    """
    findings: list[Finding] = []
    cap = spec.length_caps.get(audience)
    if cap is not None:
        words = sum(
            len(line.split())
            for number, line in enumerate(doc.lines, start=1)
            if number not in doc.fenced_lines
        )
        if words > cap:
            findings.append(
                Finding(
                    code="LENGTH_EXCEEDED",
                    severity="medium",
                    line=None,
                    heading=None,
                    rule="length cap for the audience",
                    message=(
                        f"{words} words outside code blocks; the {spec.type} template caps "
                        f"{audience} documents at {cap}"
                    ),
                )
            )
    first_match: dict[int, Heading] = {}
    for heading in doc.headings:
        index = _match_section(heading, spec)
        if index is not None:
            first_match.setdefault(index, heading)
    for index, section in enumerate(spec.sections):
        section_cap = section.max_words.get(audience)
        if section_cap is None or index not in first_match:
            continue
        heading = first_match[index]
        section_words = sum(
            len(line.split())
            for offset, line in enumerate(heading.section.split("\n"), start=1)
            if heading.line + offset not in doc.fenced_lines
        )
        if section_words <= section_cap:
            continue
        findings.append(
            Finding(
                code="LENGTH_EXCEEDED",
                severity="medium",
                line=heading.line,
                heading=heading.text,
                rule="length cap for the audience",
                message=(
                    f"{section_words} words outside code blocks under {heading.text!r}; the "
                    f"{spec.type} template caps that section at {section_cap} for {audience}"
                ),
            )
        )
    return findings


def check_document(text: str, spec: TemplateSpec, audience: str | None = None) -> list[Finding]:
    """Run every structural check over ``text`` for one audience, the template's by default."""
    if audience is None:
        audience = spec.default_audience
    if audience not in AUDIENCES:
        raise ValueError(f"unknown audience {audience!r}; audiences are {_audience_list()}")
    doc = parse_document(text)
    findings: list[Finding] = []
    findings.extend(check_sections(doc, spec))
    findings.extend(check_evidence(doc, spec))
    findings.extend(check_bans(doc, spec))
    findings.extend(check_summary(doc, spec))
    findings.extend(check_procedure(doc, spec))
    findings.extend(check_length(doc, spec, audience))
    return findings


def main(argv: list[str] | None = None) -> int:
    """Check one document against one template and print a JSON report.

    Exit 0 when the document passes, 1 when it has findings, and 2 when the apparatus fails
    (a template that does not load, a document that cannot be read, an unknown audience).
    An apparatus failure prints ``{"error": ...}``; no traceback reaches either stream.
    """
    parser = argparse.ArgumentParser(
        prog="check_structure.py",
        description="Check a Markdown document against a technical-writer template.",
    )
    parser.add_argument("--template", required=True, help="path to the template file")
    parser.add_argument("--audience", help=f"one of: {_audience_list()} (default: the template's)")
    parser.add_argument("document", help="path to the Markdown document to check")
    args = parser.parse_args(argv)

    try:
        spec = load_template(args.template)
    except (TemplateError, OSError) as exc:
        return _apparatus(str(exc))
    audience = args.audience or spec.default_audience
    if audience not in AUDIENCES:
        return _apparatus(f"unknown audience {audience!r}; audiences are {_audience_list()}")
    try:
        text = Path(args.document).read_text(encoding="utf-8")
    except OSError as exc:
        return _apparatus(f"cannot read document {args.document}: {exc.strerror or exc}")
    except UnicodeDecodeError as exc:
        return _apparatus(
            f"document {args.document} is not UTF-8 text ({exc.reason} at byte {exc.start})"
        )

    findings = check_document(text, spec, audience)
    counts = {severity: 0 for severity in SEVERITIES}
    for finding in findings:
        counts[finding.severity] += 1
    passed = passes(findings)
    report = {
        "template": spec.type,
        "audience": audience,
        "pass": passed,
        "findings": [finding.to_dict() for finding in findings],
        "counts": counts,
    }
    print(json.dumps(report, indent=2))
    return 0 if passed else 1


def _apparatus(message: str) -> int:
    print(json.dumps({"error": message}, indent=2))
    return 2


_LIST_ITEM = re.compile(r"^(\d+)[.)][ \t]+(.*)$")
_CONTINUATION = re.compile(r"^(?:[ ]{2,}|\t)\S")
_ADMONITION = re.compile(r"^(?:>\s*)?\*\*(?:Warning|Caution)\b", re.IGNORECASE)
_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
STEP_WORD_CAP = 20
STEP_SENTENCE_CAP = 2


@dataclass(frozen=True)
class _Block:
    kind: str  # "item" or "para"
    line: int
    text: str


def check_procedure(doc: Document, spec: TemplateSpec) -> list[Finding]:
    """Apply the procedure rules (spec R6) to every heading of the section the template names.

    ``procedure_section`` is a template section's label: its heading, its label key, or its
    heading_pattern's text. A heading-named section is one heading in the document; a
    pattern-named section is every heading the pattern matches, each a procedure of its own
    (the task sections of a multiple-task procedure). The rules: a stem sentence beginning
    with "To" as the last paragraph before the first step, an admonition before step 1 never
    counting as that paragraph; a first sentence of at most 20 words per step; at most two
    sentences per step (the action and its expected result); and every bold Warning or
    Caution paragraph placed before a step, never after the last one. The rules read the
    whole section, subheadings included. A template with ``procedure`` false has none.
    """
    if not spec.procedure:
        return []
    index = next(
        (i for i, section in enumerate(spec.sections) if section.label == spec.procedure_section),
        None,
    )
    targets = [h for h in doc.headings if _match_section(h, spec) == index]
    skipped = doc.fenced_lines | {heading.line for heading in doc.headings}
    findings: list[Finding] = []
    for section in targets:
        findings.extend(_procedure_findings(section, skipped))
    return findings


def _procedure_findings(section: Heading, skipped: frozenset[int]) -> list[Finding]:
    """The procedure findings for one heading's section, in document order."""
    blocks = _blocks(section, skipped)
    items = [block for block in blocks if block.kind == "item"]
    if not items:
        return []
    findings: list[Finding] = []
    rule_stem = "stem sentence beginning with To, its own paragraph, ending in a colon or a period"
    first_item_index = blocks.index(items[0])
    stem = next(
        (
            block
            for block in reversed(blocks[:first_item_index])
            if block.kind == "para" and not _ADMONITION.match(block.text)
        ),
        None,
    )
    if stem is None:
        findings.append(
            Finding(
                code="STEM_MISSING",
                severity="medium",
                line=section.line,
                heading=section.text,
                rule=rule_stem,
                message=(
                    f"section {section.text!r} opens its steps with no stem sentence; write "
                    f"one beginning with To before the first step"
                ),
            )
        )
    else:
        stem_text = _strip_markup(stem.text).strip()
        if not stem_text.startswith("To "):
            stem_problem = (
                f"line {stem.line}: the paragraph before the first step is the stem and must "
                f"begin with To; a sentence before it goes in its own paragraph"
            )
        elif not stem_text.endswith((":", ".")):
            stem_problem = f"line {stem.line}: the stem sentence must end in a colon or a period"
        else:
            stem_problem = None
        if stem_problem is not None:
            findings.append(
                Finding(
                    code="STEM_MISSING",
                    severity="medium",
                    line=stem.line,
                    heading=section.text,
                    rule=rule_stem,
                    message=stem_problem,
                )
            )
    for item in items:
        sentences = [s for s in _SENTENCE_SPLIT.split(_strip_markup(item.text)) if s.strip()]
        first_words = len(sentences[0].split()) if sentences else 0
        if first_words > STEP_WORD_CAP:
            findings.append(
                Finding(
                    code="STEP_TOO_LONG",
                    severity="medium",
                    line=item.line,
                    heading=section.text,
                    rule=f"step sentence under {STEP_WORD_CAP + 1} words",
                    message=(
                        f"line {item.line}: the step's first sentence has {first_words} words; "
                        f"the cap is {STEP_WORD_CAP}"
                    ),
                )
            )
        if len(sentences) > STEP_SENTENCE_CAP:
            findings.append(
                Finding(
                    code="STEP_TOO_MANY_SENTENCES",
                    severity="medium",
                    line=item.line,
                    heading=section.text,
                    rule="one action and one expected result per step",
                    message=(
                        f"line {item.line}: the step has {len(sentences)} sentences; write "
                        f"one action and, when the outcome is not obvious, one expected result"
                    ),
                )
            )
    last_item_index = blocks.index(items[-1])
    for block in blocks[last_item_index + 1 :]:
        if block.kind == "para" and _ADMONITION.match(block.text):
            findings.append(
                Finding(
                    code="WARNING_AFTER_STEP",
                    severity="medium",
                    line=block.line,
                    heading=section.text,
                    rule="warning before the step it protects",
                    message=(
                        f"line {block.line}: a warning or caution follows the last step; place "
                        f"it before the step it protects"
                    ),
                )
            )
    return findings


def _blocks(section: Heading, skipped: frozenset[int]) -> list[_Block]:
    """Split a section into ordered-list items and paragraphs.

    ``skipped`` holds the line numbers that are neither: fenced lines and subheadings.
    """
    blocks: list[_Block] = []
    current: _Block | None = None
    after_blank = False
    for offset, line in enumerate(section.section.split("\n"), start=1):
        number = section.line + offset
        if number in skipped:
            continue
        if not line.strip():
            after_blank = True
            if current is not None and current.kind == "para":
                blocks.append(current)
                current = None
            continue
        item = _LIST_ITEM.match(line)
        if item is not None:
            if current is not None:
                blocks.append(current)
            current = _Block(kind="item", line=number, text=item.group(2).strip())
        elif (
            current is not None
            and current.kind == "item"
            and (_CONTINUATION.match(line) or not after_blank)
        ):
            current = _Block(kind="item", line=current.line, text=f"{current.text} {line.strip()}")
        elif current is not None and current.kind == "para":
            current = _Block(kind="para", line=current.line, text=f"{current.text} {line.strip()}")
        else:
            if current is not None:
                blocks.append(current)
            current = _Block(kind="para", line=number, text=line.strip())
        after_blank = False
    if current is not None:
        blocks.append(current)
    return blocks


def _strip_markup(text: str) -> str:
    """Blank inline code to one token, drop the ``[UNVERIFIED: ...]`` markers, and drop bold
    and italic markers before counting. A marker names a missing fact; it is not a sentence of
    the step and its words are not the step's."""
    text = UNVERIFIED.sub("", _INLINE_CODE.sub("code", text))
    text = re.sub(r"[ \t]+(?=[.!?,;:])", "", text)  # no stranded period where a marker was
    return re.sub(r"[*_]{1,2}", "", text).strip()


if __name__ == "__main__":
    sys.exit(main())
