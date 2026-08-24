from __future__ import annotations

import re
import uuid
from pathlib import Path

from jiuwen_deepresearch.config import AppConfig
from jiuwen_deepresearch.engines.deepsearch import DeepSearchEngine
from jiuwen_deepresearch.engines.dry_run import DryRunEngine
from jiuwen_deepresearch.intent import compose_research_query, parse_intent
from jiuwen_deepresearch.models import Depth, Goal, Horizon, Intent, ResearchResult
from jiuwen_deepresearch.render import render_brief
from jiuwen_deepresearch.templates import load_system_prompt, load_template


def build_engine(config: AppConfig):
    if config.engine == "deepsearch":
        return DeepSearchEngine(config)
    return DryRunEngine()


async def run_research(
    query: str,
    config: AppConfig,
    *,
    goal: Goal | None = None,
    depth: Depth | None = None,
    horizon: Horizon | None = None,
    audience: str | None = None,
    constraints: str | None = None,
    conversation_id: str | None = None,
) -> tuple[Intent, ResearchResult, Path]:
    intent = parse_intent(
        query,
        goal=goal,
        depth=depth,
        horizon=horizon,
        audience=audience,
        constraints=constraints,
    )
    template = load_template(intent.goal, config.root)
    system = load_system_prompt(config.root)
    engine_query = compose_research_query(intent)
    if config.engine == "deepsearch":
        engine_query = f"{system}\n\n{engine_query}"
    cid = conversation_id or str(uuid.uuid4())
    engine = build_engine(config)
    result = await engine.run(engine_query, template, cid)
    markdown = render_brief(intent, result)
    out_dir = config.output_path
    out_dir.mkdir(parents=True, exist_ok=True)
    filename = _slug(f"{intent.goal}-{intent.topic}") + ".md"
    path = out_dir / filename
    path.write_text(markdown, encoding="utf-8")
    return intent, result, path


def _slug(text: str) -> str:
    compact = re.sub(r"[^\w\u4e00-\u9fff]+", "-", text).strip("-")
    return compact[:80] or "brief"
