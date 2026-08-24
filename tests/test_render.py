from jiuwen_deepresearch.intent import parse_intent
from jiuwen_deepresearch.models import ResearchResult
from jiuwen_deepresearch.render import render_brief


def test_render_contains_metadata():
    intent = parse_intent("智算基础设施投入的决策要点", goal="brief", audience="院所领导")
    result = ResearchResult(
        markdown="# 一句话结论\n\n先小范围试点。",
        conversation_id="cid-1",
        engine="dry-run",
    )
    text = render_brief(intent, result)
    assert "汇报简报" in text
    assert "院所领导" in text
    assert "cid-1" in text
