import asyncio

from jiuwen_deepresearch.config import load_config
from jiuwen_deepresearch.eval.golden import GOLDEN_QUERIES
from jiuwen_deepresearch.workflow import run_research


def test_golden_queries_produce_markdown(tmp_path, monkeypatch):
    config = load_config()
    config.engine = "dry-run"
    config.output_dir = str(tmp_path)

    async def _run():
        paths = []
        for query, mode in GOLDEN_QUERIES:
            intent, result, path = await run_research(query, config, goal=mode)
            assert intent.goal == mode
            assert result.engine == "dry-run"
            text = path.read_text(encoding="utf-8")
            assert intent.topic in text or query[:8] in text
            assert "dry-run" in text
            paths.append(path)
        return paths

    paths = asyncio.run(_run())
    assert len(paths) == 5
