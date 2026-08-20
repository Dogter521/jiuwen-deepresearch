# 面向领导的 AI 知识 Deep Research Agent
# 开源调研与建设规划报告

| 项目 | 说明 |
|------|------|
| 项目目录 | `jiuwen-deepresearch` |
| 版本 | v1.0 |
| 日期 | 2026-08-20 |
| 调研对象 | [github.com/openJiuwen-ai](https://github.com/openJiuwen-ai/)（19 个公开仓） |
| 状态 | 调研完成，待进入 Phase 0 环境验证 |

---

## 摘要（先看这一页）

本项目要做的不是再写一篇学术综述，而是一个**给领导用的深度研究 Agent**：把 AI 知识与面上科研收成「能拍板」的简报——一句话结论、一页要点、证据链、风险与 30/90 天动作。

对 [openJiuwen](https://github.com/openJiuwen-ai/) 19 个公开仓的调研结论如下。

**现在就要用**

- **agent-core**（PyPI 包 `openjiuwen`）：Agent / 工作流 / 工具 / LLM 的骨架，自带进程内执行引擎。
- **deepsearch**：现成的深度研究引擎（查询规划、多源检索、理解反思、片段级引用、模板化研报）。官方场景已覆盖学术与政策研究，与本项目高度同构。**不要重写这条链路。**

**明确可复用、但推迟**

- agent-runtime：生产部署平台，不是执行引擎。对外提供服务时再上。
- agent-studio / agent-memory / jiuwenswarm / skillhub：可视化运营、长期记忆、飞书企微入口、Skill 分发，按需第二期接入。

**不要整仓接入**

- sciencediscovery 面向研究者做实验（写代码、沙箱、调参），与「向上收到决策层」相反，只可借鉴文献连接器。
- Java 双栈、具身、协议 C++、vLLM 调度、大赛仓等与本项目无关。

**对本项目的一句话策略：** 在 DeepSearch 之上做薄业务层——领导三种模板（汇报 / 学习 / 立项）、意图槽位、证据口径——而不是再造检索引擎。

---

## 1. 项目定位

### 1.1 要解决什么

| 领导问法 | Agent 应交付的形态 |
|---------|-------------------|
| AI 现在到哪一步了？ | 技术成熟度地图 + 可信度标注 |
| 我们该投什么方向？ | 机会窗口 / 风险 / 竞品与政策约束 |
| 某领域论文或项目在说什么？ | 三层摘要：一句话 → 一页简报 → 证据链 |
| 面上科研怎么布局？ | 问题树、关键路径、资源与人才缺口 |

**「面上科研」统一口径（建议）：**

1. 面向上层决策的科研认知：趋势、格局、瓶颈、可落地路径。
2. 可映射到基金 / 规划语境：问题提出、研究意义、技术路线、预期成果。
3. 刻意控制深度：默认到「能拍板」，按需下钻到「能答辩」。

### 1.2 非目标

- 替代领域专家做最终学术判断
- 无引用的「自信胡编」
- 一次对话输出几十页无人读的长文
- 第一期与具体业务系统深度耦合

### 1.3 验收标准

- 典型问题（如「多模态大模型在医疗影像的机会与风险」）能产出：领导简报 + 证据清单 + 后续追问入口
- 每条关键结论可回溯到来源（论文 / 报告 / 政策 / 网页）
- 支持多轮：收窄、加深、对比、改写成汇报口径
- 架构上可见地复用 openJiuwen，而不是另起炉灶

---

## 2. openJiuwen 生态是什么

openJiuwen 是分层 Agent 平台，不是单一框架。社区主页：[openjiuwen.com](https://www.openjiuwen.com)，代码镜像同时存在于 GitHub 与 GitCode。

| 层 | 作用 | 代表仓库 |
|----|------|----------|
| Deep Agents | 面向场景的成品智能体 | deepsearch、jiuwenswarm、sciencediscovery、jiuwensymbiosis |
| Agent Studio | 低码 / 零码可视化开发与资源管理 | agent-studio |
| Agent Framework | SDK、记忆、协议 | agent-core、agent-core-java、agent-memory、agent-protocol |
| Distributed Runtime | 从开发态到生产态 | agent-runtime、agent-runtime-java、agent-dx |
| 生态与治理 | Skill 分发、文档、社区 | skillhub、docs、community |

**关键纠正：** `agent-core` 已包含进程内执行引擎（图执行、ReAct / Workflow、流式、中断恢复）。`agent-runtime` 是服务化部署平台（subprocess / Docker / K8s、REST 发布、多租户），不是「多步思考发动机」。

---

## 3. 19 个仓库调研与可用性

星标以 GitHub 2026-08-20 快照为准。可用性看：是否活跃、文档能否跟上、能否 pip 或源码跑通。GitCode 星标普遍更高，社区主阵地之一在国内镜像。

### 3.1 现在就要用

**agent-core**（Python，★426，Apache-2.0）

- 官方核心 SDK，`pip install -U openjiuwen`。Python ≥3.11 且 <3.14，推荐 3.11.4。
- 提供 ReActAgent、WorkflowAgent、工具调用、异步图执行、流式与 checkpoint。
- 本项目的 Agent / Tool / 会话都应挂在这层。DeepSearch 也基于它。
- 可用性：高。有 PyPI，持续推送。默认分支 `develop`。

**deepsearch**（Python，★115，README 称 Apache-2.0）

- 知识增强深度检索与研究引擎：查询规划 → 信息收集 → 理解反思 → 报告生成。
- 卖点：片段级引用、溯源推理、按样例 / 模板生成研报；支持本地知识库与网页融合检索。
- 官方场景：金融研报、学术与政策研究——与「领导面上科研」同构。
- 仓内还含 `codesearch/`、`base/`；近期在合入目标论文精确识别与引用传递。
- 已验证模型：Qwen3-Max（推荐）、GLM-5 / 5.1、DeepSeek V3.2、Kimi-K2.5。
- 注意：除 HITL / 终止外，SDK `run` 每次需不同 `conversation_id`。GitHub license 元数据为空，落地前核对 LICENSE。
- **结论：首选复用对象。我们做模板与口径，不重写引擎。**

### 3.2 可复用、第二期再接

| 仓库 | 作用 | 何时用 | 可用性 |
|------|------|--------|--------|
| agent-runtime ★12 | 部署、会话、生命周期；管理口默认 8186 | 给领导提供稳定 HTTP 服务、对接 Studio 发布 | 中；Docker/K8s 仍在完善 |
| agent-studio ★152 | 低码配模型、知识库、工作流 | 需要运营配置界面时 | 中高，栈重（JDK17、MySQL、Redis） |
| agent-memory ★51 | 长期记忆，`pip install JiuwenMemory` | 要记住领导偏好、禁忌词、关注领域时 | 高 |
| jiuwenswarm ★3167 | 旗舰多 Agent + 飞书 / 钉钉 / 企微等通道 | 领导要在 IM 里提问时，作渠道层，不当研究引擎 | 最高 |
| skillhub ★24 | Skill 托管分发 | 把简报 / 立项口径做成可内部分发的 Skill 时 | 中 |

### 3.3 只借鉴、不接入

**sciencediscovery**（★39）：一站式科研工作站，覆盖文献阅读、假设、写代码、沙箱实验、调参。面向研究者「往下做实验」，本项目面向领导「往上做决策」。文献 Connector 以后可参考，不宜整仓嵌入。运行依赖 Linux + bubblewrap，不是 macOS 桌面默认路径。

### 3.4 本项目跳过

| 仓库 | 原因 |
|------|------|
| agent-core-java / agent-runtime-java | 本项目走 Python + DeepSearch |
| agent-protocol | MCP / A2A 的 C++ SDK，非研究能力 |
| agent-dx | Runtime 的分布式执行底座，规模化之后才需要 |
| agent-tools | 推理路由与 vLLM 亲和调度，不是搜索工具箱 |
| jiuwensymbiosis | 具身 / Physical AI |
| relay | 多 Agent 协作开发与 Code Review |
| CareerSim-BDCI26 | 2026 大赛赛题 |
| docs / community / .github | 文档与治理，可读但不是运行依赖 |
| agent-gateway | GitCode 标明 Opening Soon |

GitCode 提到的 agent-store 在 GitHub 当前 19 仓列表中未见，暂不计入可依赖项。

---

## 4. 建设策略与架构（调研后修正）

### 4.1 相对初版规划的修正

| 初版假设 | 实际情况 |
|---------|----------|
| 用 agent-runtime 做多步 plan-act-observe | 多步执行在 agent-core；runtime 是部署平台 |
| 在 deepsearch 之上自建整条研究工作流 | DeepSearch 已经是规划-检索-反思-带引用成稿；应定制而非重写 |
| 三种模式要全新实现 | 对齐 DeepSearch「按模板 / 样例生成报告」，做成三套模板即可 |

### 4.2 建议架构

```
领导 Deep Research 业务层（本仓库 jiuwen-deepresearch）
        |  意图槽位 / 三种模板 / 面上口径 / 证据规则
        v
   deepsearch（研究引擎，开箱即用）
        |
        v
   agent-core / openjiuwen SDK
        |
        +-- LLM API（优先官方已验证模型，如 Qwen3-Max）
        +-- 后期可选：agent-runtime 发布、memory、Swarm 渠道
```

原则：业务逻辑放在本仓库薄层；执行与检索跟随上游升级。

### 4.3 三种模式（做成 DeepSearch 模板）

| 模式 | 目标 | 输出偏重 |
|------|------|----------|
| 汇报 | 开会用 | 1 页简报 + 3 条建议 + 风险 |
| 学习 | 补齐认知 | 概念阶梯 + 类比 + 必读清单 |
| 立项 / 面上 | 写意义与路线 | 问题提出 → 意义 → 路线 → 指标 → 风险 |

固定章节建议：一句话结论；背景与为何现在重要；技术 / 产业 / 政策三棱镜；关键判断（带置信度）；风险与误区；建议动作（30 天 / 90 天）；附录来源与术语表。

### 4.4 工作流（复用 DeepSearch，叠加领导策略）

1. 意图澄清：决策 / 学习 / 立项；时间范围；深度 L1 简报 / L2 标准 / L3 深潜
2. 查询规划：拆成技术、产业、政策、竞品、风险子问题；中英检索词
3. DeepSearch 广搜与融合检索
4. 来源分层配额：学术 / 产业 / 政策，每层保底，避免单一信源偏见
5. 精读抽取：主张、证据、反证、适用边界
6. 交叉验证：标注共识 / 争议 / 未知
7. 按所选模板成稿并改写口径
8. 多轮修订：更短、更偏产业、对比、改成口播

证据规则：无来源不得写事实断言；置信度高 / 中 / 低显式标注；冲突必须呈现，不得静默择一。

---

## 5. 实施路线

| 阶段 | 周期 | 做什么 |
|------|------|--------|
| Phase 0 摸底 | 0.5–1 天 | 锁定 `openjiuwen` 与 deepsearch 版本；按 SDK 跑通一条学术 / 政策样例；整理 API 对照（run、conversation_id、模板、引用结构） |
| Phase 1 MVP | 3–5 天 | 意图槽位 + 三套领导模板；打通澄清 → 检索 → 抽取 → 成稿；输出带来源的 Markdown 简报；5 条黄金问题手工验收 |
| Phase 2 强化 | 约 1 周 | 来源配额、冲突与置信度、精读预算、进度展示、面上立项改写 |
| Phase 3 可信 | 持续 | 评测集（医疗 AI、具身、智算、对齐等）、PPT 大纲导出、可选内网知识库 |

MVP **不上** agent-runtime。本地脚本或 CLI 调用 DeepSearch 即可。

---

## 6. 风险与待决策

| 风险 | 对策 |
|------|------|
| 检索噪声导致简报误导 | 权威源分层配额 + 冲突展示 |
| 模型幻觉、领导信任崩塌 | 强制引用；无证据标「未知」 |
| 时延过长 | 先出 L1 快报，后台继续 L2 |
| 上游 API 变动 | 业务层只依赖薄适配器 |
| 「面上」口径歧义 | 以本报告第 1.1 节为准，产品评审确认 |

**需要拍板的事项：**

1. 部署形态：本地 CLI 优先，还是要 Web？
2. 模型：云端 API 还是本地 / 专有？是否必须国产化？
3. 「面上科研」以决策简报为主，还是要贴近基金申请书结构？
4. 检索是否必须覆盖 arXiv / CNKI / 政策库？有无内网资料？
5. 版本锁定：pin 到哪一个 release / commit？

---

## 7. 建议的下一步

1. 确认第 6 节决策项（尤其是口径与检索范围）。
2. 进入 Phase 0：安装 agent-core 与 deepsearch，跑通官方样例。
3. 在本仓库落地三套领导模板，用 1–2 个真实领导问题打通全链路。

---

## 附录 A  仓库一览（GitHub，2026-08-20）

| 仓库 | 语言 | ★ | 本项目态度 |
|------|------|--:|------------|
| jiuwenswarm | Python | 3167 | 第二期渠道 |
| agent-core | Python | 426 | 现在用 |
| agent-studio | Java | 152 | 第二期可选 |
| deepsearch | Python | 115 | 现在用 |
| agent-protocol | C++ | 79 | 跳过 |
| jiuwensymbiosis | Python | 52 | 跳过 |
| agent-memory | Python | 51 | 第二期可选 |
| sciencediscovery | TypeScript | 39 | 只借鉴 |
| agent-core-java | Java | 31 | 跳过 |
| docs | Markdown | 30 | 参考文档 |
| skillhub | Python | 24 | 第二期可选 |
| agent-runtime-java | Java | 23 | 跳过 |
| agent-tools | Python | 17 | 跳过 |
| community | — | 12 | 治理材料 |
| agent-runtime | Python | 12 | 服务化时再用 |
| CareerSim-BDCI26 | Python | 5 | 跳过 |
| relay | TypeScript | 4 | 跳过 |
| .github | — | 3 | 跳过 |
| agent-dx | Python | 0 | 跳过 |

## 附录 B  资料来源

- GitHub 组织页与 REST API：`https://github.com/openJiuwen-ai`、`https://api.github.com/orgs/openJiuwen-ai/repos`
- GitCode 组织总览与各仓 README：`https://gitcode.com/openJiuwen`
- 官方站点：`https://www.openjiuwen.com`
- agent-core / deepsearch / agent-runtime / agent-studio / agent-memory / jiuwenswarm / skillhub / sciencediscovery 各仓 README（调研当日）
