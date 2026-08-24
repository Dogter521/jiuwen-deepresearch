from __future__ import annotations

from pathlib import Path

import yaml

from jiuwen_deepresearch.config import ROOT
from jiuwen_deepresearch.models import Goal


def load_template(goal: Goal, root: Path | None = None) -> str:
    root = root or ROOT
    modes = yaml.safe_load((root / "configs" / "modes.yaml").read_text(encoding="utf-8"))
    rel = modes[goal]["template"]
    path = root / rel
    return path.read_text(encoding="utf-8")


def load_system_prompt(root: Path | None = None) -> str:
    root = root or ROOT
    return (root / "prompts" / "system_leader.md").read_text(encoding="utf-8")
