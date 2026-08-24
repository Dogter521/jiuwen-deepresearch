from __future__ import annotations

import re

from jiuwen_deepresearch.models import Depth, Goal, Horizon, Intent

_GOAL_HINTS: list[tuple[Goal, tuple[str, ...]]] = [
    ("proposal", ("立项", "面上", "基金", "申请书", "技术路线", "研究意义")),
    ("learn", ("学习", "是什么", "讲清楚", "补齐", "概念", "入门", "科普")),
    ("brief", ("汇报", "开会", "简报", "决策", "该不该", "机会与风险", "投入")),
]

_DEPTH_HINTS: list[tuple[Depth, tuple[str, ...]]] = [
    ("L1", ("一页", "简报", "尽快", "口头", "会上")),
    ("L3", ("深潜", "详细", "完整", "答辩", "长报告")),
]

_HORIZON_HINTS: list[tuple[Horizon, tuple[str, ...]]] = [
    ("6m", ("半年", "近6月", "最近", "当下")),
    ("5y+", ("五年", "中长期", "十年")),
    ("1-3y", ("三年", "1-3年", "两到三年")),
]


def parse_intent(
    query: str,
    *,
    goal: Goal | None = None,
    depth: Depth | None = None,
    horizon: Horizon | None = None,
    audience: str | None = None,
    constraints: str | None = None,
) -> Intent:
    text = query.strip()
    if not text:
        raise ValueError("查询不能为空")

    inferred_goal = goal or _infer(text, _GOAL_HINTS, "brief")
    default_depth: Depth = "L1" if inferred_goal == "brief" else "L2"
    inferred_depth = depth or _infer(text, _DEPTH_HINTS, default_depth)
    inferred_horizon = horizon or _infer(text, _HORIZON_HINTS, "1-3y")

    topic = _strip_mode_words(text)
    return Intent(
        goal=inferred_goal,
        topic=topic,
        horizon=inferred_horizon,
        audience=(audience or "院所领导").strip() or "院所领导",
        constraints=(constraints or "").strip(),
        depth=inferred_depth,
        raw_query=text,
    )


def compose_research_query(intent: Intent) -> str:
    report_type = {"L1": "精简版", "L2": "专业版", "L3": "专业版"}[intent.depth]
    horizon_text = {"6m": "近 6 个月", "1-3y": "未来 1 到 3 年", "5y+": "5 年及以上"}[intent.horizon]
    extra = f"约束：{intent.constraints}。" if intent.constraints else ""
    return (
        f"请写一份{report_type}报告，面向{intent.audience}，语气正式且偏分析。"
        f"时间范围关注{horizon_text}。模式为{intent.mode_label}。"
        "必须区分学术、产业、政策来源；无证据写未知；冲突单独列出；"
        "关键判断标注置信度高/中/低；建议动作分成 30 天与 90 天。"
        f"{extra}研究主题：{intent.topic}"
    )


def _infer(text: str, table: list[tuple[str, tuple[str, ...]]], default: str) -> str:
    for value, hints in table:
        if any(h in text for h in hints):
            return value
    return default


def _strip_mode_words(text: str) -> str:
    cleaned = text
    for word in ("请写一份", "请给我", "帮我", "汇报模式", "学习模式", "立项模式"):
        cleaned = cleaned.replace(word, "")
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" ：:，,。")
    return cleaned or text
