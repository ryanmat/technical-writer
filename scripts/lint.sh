#!/bin/sh
# Description: Runs the optional prose and Markdown linters over one document when they are
# Description: on PATH, and prints one JSON object naming what ran, what was missing, and each tool's output.
#
# Usage: sh scripts/lint.sh <document.md>
#
# Detects vale, markdownlint and markdownlint-cli2 (the last two reported under the name
# markdownlint), runs those present with the configs beside the skill, and exits 0 when every
# tool that ran exited 0, 1 when one did not, 2 when the document is missing. A missing tool,
# or one on PATH that could not run (reported under notes), is never an error: the by-hand
# checklist in references/checklists.md covers it.

set -u

# The script's directory without dirname, so the only external command needed is awk.
case "$0" in */*) script_dir=${0%/*} ;; *) script_dir=. ;; esac
plugin_root=$(CDPATH= cd -- "$script_dir/.." && pwd)
references="$plugin_root/skills/technical-writer/references"
vale_config="$references/vale/.vale.ini"
markdownlint_config="$references/markdownlint.jsonc"

usage() {
    printf 'Usage: sh scripts/lint.sh <document.md>\n'
    printf 'Runs vale and markdownlint (or markdownlint-cli2) over the document when present\n'
    printf 'and prints one JSON object: document, ran, missing, notes, checklist, results.\n'
}

# json_string <text>: the text as a JSON string literal, backslash, quote, tab, CR and
# newline escaped; other control characters are not expected in linter output.
json_string() {
    printf '%s' "$1" | awk '
        BEGIN { ORS = ""; printf "\"" }
        {
            gsub(/\\/, "\\\\"); gsub(/"/, "\\\""); gsub(/\t/, "\\t"); gsub(/\r/, "\\r")
            if (NR > 1) printf "\\n"
            printf "%s", $0
        }
        END { printf "\"" }'
}

# json_list <name>...: a JSON array of the names, empty when none.
json_list() {
    out="["
    sep=""
    for item in "$@"; do
        out="$out$sep$(json_string "$item")"
        sep=","
    done
    printf '%s]' "$out"
}

error() {
    printf '{"error": %s}\n' "$(json_string "$1")"
    exit 2
}

case "${1:-}" in
    -h|--help) usage; exit 0 ;;
    "") error "no document argument: the path of one Markdown file is required" ;;
esac
document=$1
[ -f "$document" ] || error "document not found: $document"

ran=""
missing=""
results=""
notes=""
status=0

# record <name> <exit> <output>: appends one results entry and tracks the overall status.
record() {
    entry="$(json_string "$1"): {\"exit\": $2, \"output\": $(json_string "$3")}"
    results="$results${results:+, }$entry"
    ran="$ran${ran:+ }$1"
    [ "$2" -eq 0 ] || status=1
}

# not_ready <name> <note>: a linter on PATH that could not run counts as missing, with the
# note saying why and what makes it ready; a missing linter never fails the script.
not_ready() {
    missing="$missing${missing:+ }$1"
    notes="$notes${notes:+, }$(json_string "$1"): $(json_string "$2")"
}

if command -v vale >/dev/null 2>&1; then
    output=$(vale --config "$vale_config" --output JSON "$document" 2>&1)
    code=$?
    if [ "$code" -eq 2 ]; then
        # Vale exits 2 on a configuration or runtime error (E-codes), such as a package the
        # ini names that vale sync has not fetched; its output is the error, not findings.
        not_ready vale "vale could not run (exit 2): $output. For a package the ini names, run: vale --config $vale_config sync"
    else
        record vale "$code" "$output"
    fi
else
    missing="$missing${missing:+ }vale"
fi

if command -v markdownlint >/dev/null 2>&1; then
    output=$(markdownlint --config "$markdownlint_config" "$document" 2>&1)
    record markdownlint $? "$output"
elif command -v markdownlint-cli2 >/dev/null 2>&1; then
    output=$(markdownlint-cli2 --config "$markdownlint_config" "$document" 2>&1)
    record markdownlint $? "$output"
else
    missing="$missing${missing:+ }markdownlint"
fi

if [ -n "$missing" ]; then checklist=true; else checklist=false; fi

# shellcheck disable=SC2086
printf '{"document": %s, "ran": %s, "missing": %s, "notes": {%s}, "checklist": %s, "results": {%s}}\n' \
    "$(json_string "$document")" "$(json_list $ran)" "$(json_list $missing)" "$notes" \
    "$checklist" "$results"
exit $status
