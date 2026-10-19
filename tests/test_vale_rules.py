# Description: Tests over the Vale configuration, the TechnicalWriter rule files, and the
# Description: markdownlint config under skills/technical-writer/references/.
"""The linters are optional (spec R10), so these tests assert the shape of the configuration
the skill ships, never that a linter runs: the ini parses and names the style and the Google
package, every rule file is well-formed YAML with a regex Python compiles, each R10 ban has a
rule file, and the markdownlint config turns the line-length rule off and the one-H1 rule on."""

from __future__ import annotations

import configparser
import json
import re
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
REFERENCES = ROOT / "skills" / "technical-writer" / "references"
VALE_INI = REFERENCES / "vale" / ".vale.ini"
STYLE_DIR = REFERENCES / "vale" / "styles" / "TechnicalWriter"
MARKDOWNLINT = REFERENCES / "markdownlint.jsonc"

# The R10 bans Google and Grafana do not supply, each with the rule file that carries it.
R10_BANS = {
    "em and en dashes": "Dashes.yml",
    "subjunctive should, would, could": "Subjunctive.yml",
    "we recommend": "Recommendations.yml",
    "gerund task headings": "Gerunds.yml",
    "refer to": "ReferTo.yml",
    "timeless words": "Timeless.yml",
}
REQUIRED_KEYS = ("extends", "message", "level")
LEVELS = {"suggestion", "warning", "error"}
_LINE_COMMENT = re.compile(r"^\s*//.*$", re.M)
_BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.S)


def rule_files() -> list[Path]:
    return sorted(STYLE_DIR.glob("*.yml"))


def load_rule(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict), f"{path.name}: not a mapping"
    return data


def patterns(rule: dict) -> list[str]:
    """Every regex the rule carries: existence tokens and raw fragments, substitution keys."""
    found = [*rule.get("tokens", []), *rule.get("raw", [])]
    found += list(rule.get("swap", {}))
    return found


def test_vale_ini_parses_and_names_the_style_and_the_google_package():
    text = VALE_INI.read_text(encoding="utf-8")
    parser = configparser.ConfigParser(interpolation=None)
    parser.read_string("[vale]\n" + text)  # Vale's globals precede the first section
    assert parser["vale"]["StylesPath"] == "styles"
    packages = [p.strip() for p in parser["vale"]["Packages"].split(",")]
    assert "Google" in packages, packages
    styles = [s.strip() for s in parser["*.md"]["BasedOnStyles"].split(",")]
    assert "TechnicalWriter" in styles, styles
    assert "Google" in styles, styles


def test_every_rule_file_parses_with_extends_message_and_level():
    files = rule_files()
    assert files, f"no rule files under {STYLE_DIR}"
    for path in files:
        rule = load_rule(path)
        missing = [key for key in REQUIRED_KEYS if key not in rule]
        assert not missing, f"{path.name}: missing {missing}"
        assert rule["level"] in LEVELS, f"{path.name}: level {rule['level']!r}"
        assert patterns(rule), f"{path.name}: no tokens, raw or swap"


@pytest.mark.parametrize("ban", list(R10_BANS), ids=lambda ban: ban.replace(" ", "-"))
def test_each_r10_ban_has_a_rule_file(ban: str):
    assert (STYLE_DIR / R10_BANS[ban]).is_file(), f"{ban}: no {R10_BANS[ban]}"


@pytest.mark.parametrize("path", rule_files(), ids=lambda path: path.stem)
def test_every_regex_in_a_rule_compiles(path: Path):
    for pattern in patterns(load_rule(path)):
        re.compile(pattern)


def test_markdownlint_config_parses_with_line_length_off_and_one_h1_on():
    text = MARKDOWNLINT.read_text(encoding="utf-8")
    stripped = _LINE_COMMENT.sub("", _BLOCK_COMMENT.sub("", text))
    config = json.loads(stripped)
    assert config["MD013"] is False
    assert config["MD025"] is True
