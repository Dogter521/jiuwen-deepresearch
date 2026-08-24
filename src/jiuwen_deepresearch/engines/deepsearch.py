from __future__ import annotations

import copy
import json
import os
import uuid

from jiuwen_deepresearch.config import AppConfig
from jiuwen_deepresearch.models import EvidenceItem, ResearchResult


class DeepSearchEngine:
    """Thin adapter around official openjiuwen-deepsearch SDK."""

    name = "deepsearch"

    def __init__(self, config: AppConfig):
        self.config = config

    async def run(self, query: str, template: str, conversation_id: str) -> ResearchResult:
        try:
            from openjiuwen_deepsearch.config.config import Config
            from openjiuwen_deepsearch.framework.openjiuwen.agent.agent_factory import AgentFactory
            from openjiuwen_deepsearch.framework.openjiuwen.agent.workflow import (
                parse_endnode_content,
            )
        except ImportError as exc:
            raise RuntimeError(
                "未安装 openjiuwen-deepsearch。请使用 Python 3.11–3.13，并执行 "
                "pip install -e '.[deepsearch]'"
            ) from exc

        self._require_credentials()
        os.environ.setdefault("LLM_SSL_VERIFY", os.getenv("LLM_SSL_VERIFY", "false"))
        os.environ.setdefault("TOOL_SSL_VERIFY", os.getenv("TOOL_SSL_VERIFY", "false"))

        agent_config = Config().agent_config.model_dump()
        general = copy.deepcopy(agent_config.get("llm_config", {}).get("general") or {})
        general.update(
            {
                "model_name": self.config.llm.model_name,
                "model_type": self.config.llm.model_type,
                "base_url": self.config.llm.base_url,
                "api_key": self.config.llm.api_key,
            }
        )
        agent_config.setdefault("llm_config", {})["general"] = general
        agent_config["web_search_engine_config"] = {
            **(agent_config.get("web_search_engine_config") or {}),
            "search_engine_name": self.config.search.engine_name,
            "search_url": self.config.search.search_url,
            "search_api_key": self.config.search.search_api_key,
        }
        ds = self.config.deepsearch
        agent_config["workflow_human_in_the_loop"] = ds.workflow_human_in_the_loop
        agent_config["outline_interaction_enabled"] = ds.outline_interaction_enabled
        agent_config["search_mode"] = ds.search_mode
        agent_config["execution_method"] = ds.execution_method

        cid = conversation_id or str(uuid.uuid4())
        agent = AgentFactory().create_agent(agent_config)
        report = ""
        events: list[str] = []
        async for chunk in agent.run(
            message=query,
            conversation_id=cid,
            report_template=template,
            interrupt_feedback="",
            agent_config=agent_config,
        ):
            payload = json.loads(chunk) if isinstance(chunk, str) else chunk
            if isinstance(payload, dict):
                agent_name = str(payload.get("agent") or payload.get("node") or "")
                if agent_name:
                    events.append(agent_name)
            parsed = parse_endnode_content(payload)
            if parsed:
                report = parsed if isinstance(parsed, str) else json.dumps(parsed, ensure_ascii=False)

        if not report:
            raise RuntimeError("DeepSearch 未返回最终报告。请检查模型与搜索配置。")

        return ResearchResult(
            markdown=report,
            conversation_id=cid,
            engine=self.name,
            sources=_extract_sources(report),
            events=events,
            used_template=template,
        )

    def _require_credentials(self) -> None:
        missing = []
        if not self.config.llm.api_key or not self.config.llm.base_url:
            missing.append("LLM_API_KEY / LLM_BASE_URL")
        if not self.config.search.search_api_key and self.config.search.engine_name not in {"jina"}:
            missing.append("SEARCH_API_KEY")
        if missing:
            raise RuntimeError("DeepSearch 缺少配置：" + ", ".join(missing))


def _extract_sources(markdown: str) -> list[EvidenceItem]:
    items: list[EvidenceItem] = []
    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("http://") or stripped.startswith("https://"):
            items.append(
                EvidenceItem(
                    claim="来源链接",
                    source_url=stripped,
                    confidence="medium",
                    status="unknown",
                )
            )
        elif stripped.startswith("- http"):
            url = stripped.lstrip("- ").strip()
            items.append(
                EvidenceItem(
                    claim="来源链接",
                    source_url=url,
                    confidence="medium",
                    status="unknown",
                )
            )
    return items
