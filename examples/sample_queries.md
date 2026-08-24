# 黄金问题

用于手工验收 MVP。默认引擎为 `dry-run` 时只验证意图、模板与成稿结构；配置 DeepSearch 后验证内容质量。

1. 多模态大模型在医疗影像的机会与风险（建议 `--mode brief`）
2. 具身智能现在到哪一步了，院所该不该布局（建议 `--mode brief --horizon 1-3y`）
3. 给非技术领导讲清楚什么是 Deep Research Agent（建议 `--mode learn`）
4. 面向国家自然科学基金面上项目，AI 安全对齐可以怎样提问题（建议 `--mode proposal`）
5. 智算基础设施投入的决策要点：建设、租赁还是联合（建议 `--mode brief --depth L1`）

```bash
jiuwen-research "多模态大模型在医疗影像的机会与风险" --mode brief
```
