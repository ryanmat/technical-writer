# Description: Shared helpers for the eval-harness tests: the captured plugin eval fixture's
# Description: directory and the by-path import of the modules under evals/, which is on no path.
"""Used by tests/test_run_evals.py and tests/test_gate.py, and by the fixture-orphan test."""

from __future__ import annotations

import importlib.util
import sys
from types import ModuleType

from conftest import FIXTURES_DIR, ROOT

PLUGIN_EVAL_DIR = FIXTURES_DIR / "plugin-eval"  # one captured plugin eval result, not a template


def load_evals_module(name: str) -> ModuleType:
    """Import ``evals/<name>.py`` by path, since ``evals`` is on no import path."""
    path = ROOT / "evals" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module
