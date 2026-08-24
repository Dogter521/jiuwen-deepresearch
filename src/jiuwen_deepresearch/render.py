from __future__ import annotations

from datetime import date

from jiuwen_deepresearch.models import Intent, ResearchResult


def render_brief(intent: Intent, result: ResearchResult) -> str:
    header = [
        f"# {intent.mode_label}简报：{intent.topic}",
        "",
        f"- 模式：{intent.mode_label}（{intent.goal}）",
        f"- 读者：{intent.audience}",
        f"- 深度：{intent.depth}",
        f"- 时间范围：{intent.horizon}",
        f"- 引擎：{result.engine}",
        f"- 会话：{result.conversation_id}",
        f"- 日期：{date.today().isoformat()}",
        "",
        "---",
        "",
        result.markdown.strip(),
        "",
    ]
    if result.sources and "附录" not in result.markdown:
        header.append("## 结构化来源")
        header.append("")
        for item in result.sources:
            loc = item.source_url or item.source_title or "无出处"
            header.append(
                f"- [{item.confidence}/{item.status}/{item.layer}] {item.claim} — {loc}"
            )
        header.append("")
    return "\n".join(header)
