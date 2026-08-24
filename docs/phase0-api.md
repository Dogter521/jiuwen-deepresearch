# Phase 0 API 对照

锁定版本（2026-08-24）：

- `openjiuwen` 0.1.17
- `openjiuwen-deepsearch` 0.1.9
- Python `>=3.11,<3.14`（推荐 3.11.4 / 3.12）

## 本仓库调用面

| 能力 | 接口 | 说明 |
|------|------|------|
| 配置 | `Config().agent_config.model_dump()` | 必须填 `llm_config.general`；搜索填 `web_search_engine_config` |
| 创建 | `AgentFactory().create_agent(agent_config)` | `execution_method=parallel` 得到 DeepresearchAgent |
| 运行 | `agent.run(message, conversation_id, report_template=..., agent_config=...)` | 流式 chunk；除 HITL 外每次新 `conversation_id` |
| 终稿 | `parse_endnode_content(chunk)` | 非空即为最终报告 |
| 模板 | Markdown，一级/二级标题 + `功能概述` + `是否核心章节` | 三套领导模板在 `prompts/templates/` |

查询里可直接带约束：精简版/专业版、读者、语气。本仓库的 `compose_research_query` 会自动拼这些约束。

官方已验证模型：Qwen3-Max、GLM-5 / 5.1、DeepSeek V3.2、Kimi-K2.5。
