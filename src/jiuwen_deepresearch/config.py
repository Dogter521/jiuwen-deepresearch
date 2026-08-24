from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[2]


def _load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


class LLMSettings(BaseModel):
    model_name: str = "qwen3-max"
    model_type: str = "openai"
    base_url: str = ""
    api_key: str = ""


class SearchSettings(BaseModel):
    engine_name: str = "jina"
    search_url: str = "https://s.jinaai.cn"
    search_api_key: str = ""


class DeepSearchSettings(BaseModel):
    search_mode: str = "research"
    execution_method: str = "parallel"
    workflow_human_in_the_loop: bool = False
    outline_interaction_enabled: bool = False


class AppConfig(BaseModel):
    engine: str = "dry-run"
    output_dir: str = "output"
    llm: LLMSettings = Field(default_factory=LLMSettings)
    search: SearchSettings = Field(default_factory=SearchSettings)
    deepsearch: DeepSearchSettings = Field(default_factory=DeepSearchSettings)

    @property
    def root(self) -> Path:
        return ROOT

    @property
    def output_path(self) -> Path:
        path = Path(self.output_dir)
        if not path.is_absolute():
            path = ROOT / path
        return path


def load_config(root: Path | None = None) -> AppConfig:
    root = root or ROOT
    _load_dotenv(root / ".env")
    data: dict[str, Any] = {}
    yaml_path = root / "configs" / "agent.yaml"
    if yaml_path.exists():
        loaded = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
        data.update(loaded)

    env_engine = os.getenv("JIUWEN_ENGINE")
    if env_engine:
        data["engine"] = env_engine
    if os.getenv("JIUWEN_OUTPUT_DIR"):
        data["output_dir"] = os.environ["JIUWEN_OUTPUT_DIR"]

    llm = dict(data.get("llm") or {})
    llm["model_name"] = os.getenv("LLM_MODEL_NAME", llm.get("model_name", "qwen3-max"))
    llm["model_type"] = os.getenv("LLM_MODEL_TYPE", llm.get("model_type", "openai"))
    llm["base_url"] = os.getenv("LLM_BASE_URL", llm.get("base_url", ""))
    llm["api_key"] = os.getenv("LLM_API_KEY", llm.get("api_key", ""))
    data["llm"] = llm

    search = dict(data.get("search") or {})
    search["engine_name"] = os.getenv("SEARCH_ENGINE_NAME", search.get("engine_name", "jina"))
    search["search_url"] = os.getenv("SEARCH_URL", search.get("search_url", ""))
    search["search_api_key"] = os.getenv("SEARCH_API_KEY", search.get("search_api_key", ""))
    data["search"] = search

    return AppConfig.model_validate(data)
