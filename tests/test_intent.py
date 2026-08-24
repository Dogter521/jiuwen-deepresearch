from jiuwen_deepresearch.intent import compose_research_query, parse_intent


def test_infer_proposal_mode():
    intent = parse_intent("面向国家自然科学基金面上项目，AI 安全对齐可以怎样提问题")
    assert intent.goal == "proposal"
    assert "AI 安全对齐" in intent.topic


def test_infer_learn_mode():
    intent = parse_intent("给非技术领导讲清楚什么是 Deep Research Agent")
    assert intent.goal == "learn"


def test_cli_mode_override():
    intent = parse_intent("具身智能现在到哪一步了", goal="brief", depth="L1")
    assert intent.goal == "brief"
    assert intent.depth == "L1"


def test_compose_query_contains_source_rules():
    intent = parse_intent("多模态大模型在医疗影像的机会与风险", goal="brief")
    text = compose_research_query(intent)
    assert "精简版" in text
    assert "30 天" in text
    assert "置信度" in text
