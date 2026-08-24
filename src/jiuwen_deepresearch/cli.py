from __future__ import annotations

import argparse
import asyncio
import sys

from jiuwen_deepresearch.config import load_config
from jiuwen_deepresearch.workflow import run_research

GOLDEN = [
    "多模态大模型在医疗影像的机会与风险",
    "具身智能现在到哪一步了，院所该不该布局",
    "给非技术领导讲清楚什么是 Deep Research Agent",
    "面向国家自然科学基金面上项目，AI 安全对齐可以怎样提问题",
    "智算基础设施投入的决策要点：建设、租赁还是联合",
]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="面向领导的 Deep Research CLI")
    parser.add_argument("query", nargs="?", help="研究问题")
    parser.add_argument("--mode", choices=["brief", "learn", "proposal"], help="汇报 / 学习 / 立项")
    parser.add_argument("--depth", choices=["L1", "L2", "L3"], help="简报 / 标准 / 深潜")
    parser.add_argument("--horizon", choices=["6m", "1-3y", "5y+"])
    parser.add_argument("--audience", default=None)
    parser.add_argument("--constraints", default="")
    parser.add_argument("--engine", choices=["dry-run", "deepsearch"], help="覆盖配置中的引擎")
    parser.add_argument("--list-examples", action="store_true")
    args = parser.parse_args(argv)

    if args.list_examples:
        for item in GOLDEN:
            print(f"- {item}")
        return 0
    if not args.query:
        parser.error("请提供查询，或使用 --list-examples")

    config = load_config()
    if args.engine:
        config.engine = args.engine

    intent, result, path = asyncio.run(
        run_research(
            args.query,
            config,
            goal=args.mode,  # type: ignore[arg-type]
            depth=args.depth,  # type: ignore[arg-type]
            horizon=args.horizon,  # type: ignore[arg-type]
            audience=args.audience,
            constraints=args.constraints,
        )
    )
    print(f"模式：{intent.mode_label}  深度：{intent.depth}  引擎：{result.engine}")
    print(f"会话：{result.conversation_id}")
    print(f"已写入：{path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
