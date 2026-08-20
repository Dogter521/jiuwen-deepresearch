# jiuwen-deepresearch

基于 openJiuwen，复用 `agent-core`、`agent-runtime`、`deepsearch`，面向领导场景的 AI 知识 Deep Research Agent。

帮助决策者深度理解 AI 知识与面上科研：趋势、格局、瓶颈、可落地路径；默认交付一句话结论、一页简报、证据链与后续动作。

## 目录结构

```
jiuwen-deepresearch/
├── README.md
├── docs/                 # 分析规划与产品口径
├── configs/              # 模型、超时、模式配置
├── prompts/              # System Prompt 与阶段提示词
├── schemas/              # 意图、证据、简报结构
├── src/
│   ├── agent/            # 组装 openJiuwen Agent
│   ├── tools/            # 封装 deepsearch 与本地工具
│   ├── workflow/         # Deep Research 阶段编排
│   ├── render/           # 简报 / 口播 / 立项表述
│   └── eval/             # 黄金问题集与检查
├── examples/             # 示例问题
└── tests/
```

## 当前状态

- 已完成：开源调研与建设规划报告
  - PDF：`docs/面向领导的AI知识DeepResearch建设报告.pdf`
  - Markdown：`docs/面向领导的AI知识DeepResearch建设报告.md`
- 下一步：锁定 openJiuwen 版本，跑通 DeepSearch 官方示例（Phase 0）
