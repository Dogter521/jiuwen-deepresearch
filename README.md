# jiuwen-deepresearch

面向领导的 AI 知识 Deep Research Agent。复用 openJiuwen 的 `agent-core`（PyPI：`openjiuwen`）与 `deepsearch`（PyPI：`openjiuwen-deepsearch`），在本仓库做薄业务层：意图槽位、三种领导模板、证据口径。

默认交付：一句话结论、一页简报、证据链、风险、30/90 天动作。

## 三种模式

| 模式 | 参数 | 产出 |
|------|------|------|
| 汇报 | `--mode brief` | 开会用的一页简报 |
| 学习 | `--mode learn` | 概念阶梯与必读清单 |
| 立项 | `--mode proposal` | 面上口径：问题、意义、路线、指标 |

## 快速开始（离线 MVP）

需要 Python 3.11 或 3.12（不要用 3.14，上游 SDK 不支持）。

```bash
cd jiuwen-deepresearch
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
jiuwen-research --list-examples
jiuwen-research "多模态大模型在医疗影像的机会与风险" --mode brief
```

离线默认走 `dry-run`：打通意图 → 模板 → 成稿，不调用模型和搜索。结果写在 `output/`。

## 接入真实 DeepSearch

```bash
cp .env.example .env
# 填写 LLM_BASE_URL、LLM_API_KEY，以及搜索引擎密钥
pip install -e ".[deepsearch]"
jiuwen-research "具身智能现在到哪一步了" --mode brief --engine deepsearch
```

版本锁定见 `docs/phase0-api.md`。每次新任务会生成新的 `conversation_id`。

## 目录

```
configs/                 # 引擎与模式
prompts/templates/       # 三套 DeepSearch 兼容模板
schemas/                 # 意图 / 证据 / 简报
src/jiuwen_deepresearch/ # CLI、意图、工作流、DeepSearch 适配器
examples/sample_queries.md
tests/
```

## 当前状态

- Phase 0：API 对照见 `docs/phase0-api.md`
- Phase 1 MVP：离线全链路可跑；DeepSearch 为可选引擎
- 一阶段实现报告：`docs/一阶段实现报告.md`
- 规划报告：`docs/面向领导的AI知识DeepResearch建设报告.md`
