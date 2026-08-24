from __future__ import annotations

import uuid

from jiuwen_deepresearch.models import EvidenceItem, ResearchResult


class DryRunEngine:
    """Offline engine so CLI, templates and tests work before DeepSearch is wired."""

    name = "dry-run"

    async def run(self, query: str, template: str, conversation_id: str) -> ResearchResult:
        cid = conversation_id or str(uuid.uuid4())
        topic = query
        if "研究主题：" in query:
            topic = query.split("研究主题：", 1)[1].strip()
        headings = [line[2:].strip() for line in template.splitlines() if line.startswith("# ")]
        sections = [
            f"## {title}\n\n"
            f"（dry-run）本节将在接入 DeepSearch 后按模板撰写。\n\n"
            "判断置信度：低。证据状态：未知。尚未检索学术 / 产业 / 政策来源。\n"
            for title in headings
        ]
        markdown = (
            "# 领导简报（dry-run）\n\n"
            f"> 本输出只验证意图槽位、模板与成稿结构，不构成事实判断。主题：{topic}\n\n"
            + "\n".join(sections)
            + "\n## 附录：来源与术语\n\n- 无来源。接入 DeepSearch 后将在此列出可回溯引用。\n"
        )
        return ResearchResult(
            markdown=markdown,
            conversation_id=cid,
            engine=self.name,
            sources=[
                EvidenceItem(
                    claim="尚未执行检索",
                    confidence="low",
                    status="unknown",
                    layer="unknown",
                )
            ],
            events=["intent_ready", "template_loaded", "dry_run_filled"],
            used_template=template,
        )
