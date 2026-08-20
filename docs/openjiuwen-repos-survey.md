# openJiuwen 开源仓库调研（对照本项目）

> 调研对象：[github.com/openJiuwen-ai](https://github.com/openJiuwen-ai/)（19 个公开仓）  
> 官方文档/镜像：[openjiuwen.com](https://www.openjiuwen.com)、[gitcode.com/openJiuwen](https://gitcode.com/openJiuwen)  
> 日期：2026-08-20  
> 用途：判断「面向领导的 AI 知识 Deep Research Agent」应复用什么、延后什么、不要碰什么。

---

## 1. 社区在做什么

openJiuwen 是一套**分层 Agent 平台**，不是单一框架：

| 层 | 作用 |
|----|------|
| Deep Agents | 面向场景的成品智能体（DeepSearch、JiuwenSwarm、ScienceDiscovery 等） |
| Agent Studio | 低码/零码可视化开发与资源管理 |
| Agent Framework | Python/Java SDK（agent-core）+ 记忆 + 协议 |
| Agent Distributed Runtime | 把 Agent 从开发态推到生产态（部署、多租户、生命周期） |
| Agent System Service | 沙箱、文件系统、跨 Agent 通信等（部分仍在演进） |

**对本项目最关键的纠正：**  
`agent-core` 里已经自带**进程内执行引擎**（图执行、ReAct/Workflow、流式、中断恢复）。  
`agent-runtime` **不是**这套引擎，而是**服务化部署平台**（subprocess / Docker / K8s、REST 发布、多租户）。  
前期规划里把 runtime 当成「多步执行发动机」是不准确的；Deep Research 的多步循环应落在 **agent-core + deepsearch**，runtime 留给以后给领导提供服务时再用。

---

## 2. 19 个仓库逐项说明

星标以 GitHub 2026-08-20 快照为准。GitCode 星标普遍更高（社区主阵地之一），可用性以代码是否活跃、文档是否可跟、是否能 pip/源码跑通为准。

### 2.1 与本项目强相关

#### agent-core（Python，★426，Apache-2.0）

- **干什么：** 官方核心 SDK，PyPI 包名 `openjiuwen`。提供 Agent 创建、工作流编排、LLM 调用、工具调用、ReActAgent / WorkflowAgent、异步图执行、流式、checkpoint。
- **环境：** Python ≥3.11 且 <3.14，推荐 3.11.4。`pip install -U openjiuwen`
- **对本项目：** **必须用。** DeepSearch 也基于它。领导 Agent 的 Skill/Tool/会话都应挂在这层。
- **可用性：** 高。有 PyPI、持续推送、文档与示例完整。默认分支 `develop`。

#### deepsearch（Python，★115）

- **干什么：** 知识增强的深度检索与研究引擎。多 Agent 协同：查询规划 → 信息收集 → 理解反思 → 报告生成。卖点是**片段级引用、溯源推理、模板化研报**。
- **仓内结构：** 外层聚合仓，含 `deepsearch/`（深度研究）与 `codesearch/`（代码检索）、`base/`。近期还在合入「目标论文精确识别与引用传递」。
- **场景自称：** 金融研报、学术与政策研究——与「领导面上科研认知」高度同构。
- **对本项目：** **首选复用对象，不要重写检索-规划-成稿链路。** 我们做的是：领导口径模板、意图槽位、来源分层策略、面上立项改写，挂在 DeepSearch 的报告生成层之上。
- **可用性：** 高。有完整版（带前端）安装文档（Win/Mac/Linux）和 SDK 二次开发指南。已验证模型：Qwen3-Max、GLM-5/5.1、DeepSeek V3.2、Kimi-K2.5。
- **注意：** 除 HITL/终止外，SDK `run` 每次需不同 `conversation_id`。GitHub license 元数据为空，README 写 Apache-2.0，落地前核对 LICENSE。

#### agent-runtime（Python，★12，Apache-2.0）

- **干什么：** 生产部署与生命周期：统一 REST 发布、多租户隔离、subprocess/docker/k8s。默认管理口 `8186`，Agent 侧 `/query`、`/health`。
- **对本项目：** **MVP 不必上。** 本地 CLI/脚本跑 DeepSearch 即可。要给领导做可访问服务、或对接 Studio 一键发布时再引入。
- **可用性：** 中。代码仍在推（2026-08-20 有 push），文档齐全，但 GitHub 星标低、Roadmap 写明 Docker/K8s/CLI/WebUI 仍在完善。依赖 Python≥3.11.4、uv。

### 2.2 可选增强（第二期再接）

#### agent-studio（Java + 前端，★152，Apache-2.0）

- **干什么：** 一站式低码平台：Agent/工作流可视化、模型与知识库、插件、Prompt、MCP。可把 DeepSearch 当参考 Agent 配模型/工具/知识库。
- **对本项目：** 若领导侧需要「配置知识库、选模型、看调试」的运营界面，可接；纯代码定制领导 Agent 则不必先上。
- **可用性：** 中高。功能全，但栈重（JDK17、MySQL、Redis、Docker，四个服务）。默认分支 `studio-2.0`。

#### agent-memory / JiuwenMemory（Python，★51，Apache-2.0）

- **干什么：** 长期记忆：分层 L0–L3、睡眠巩固、图谱记忆、多存储后端。`pip install JiuwenMemory`
- **对本项目：** 领导偏好（汇报口径、关注领域、禁忌词）跨会话记住时再接。单次深度研究不依赖它。
- **可用性：** 高（有 PyPI）。

#### jiuwenswarm（Python，★3167，Apache-2.0）

- **干什么：** 旗舰多 Agent 产品。Leader 拆任务组队、Skill 自演进、IM 通道（飞书/钉钉/企微/微信等）。示例任务就是「对某产业做深度研究并出分析报告」。公告称将升级为 WorkSwarm。
- **对本项目：** 不要当研究引擎用（会绑一整套工作台）。若最终交付要「领导在飞书里提问」，可作为**渠道层**包一层 DeepSearch/本 Agent。
- **可用性：** 最高（星标、桌面安装包、`pip install jiuwenswarm`）。与本项目目标重叠的是交互面，不是研究内核。

#### skillhub（Python + React，★24，Apache-2.0）

- **干什么：** Skill 托管分发（可自建，兼容 ClawHub）。官方托管 [swarmskills.openjiuwen.com](https://swarmskills.openjiuwen.com)。
- **对本项目：** 把「领导简报 / 面上立项」做成可复用 Skill 并内部分发时再考虑。MVP 用仓库内 prompts 即可。
- **可用性：** 中。依赖 MySQL + S3/MinIO。

#### sciencediscovery（TypeScript，★39，Apache-2.0）

- **干什么：** 科研工作站：文献、假设、写代码、沙箱跑实验、参数调优。面向**研究者做实验**，默认本机、非多租户。
- **对本项目：** **不要当领导简报引擎。** 定位相反：它往下钻到代码与实验，我们往上收到决策层。文献 Connector 以后可参考，不宜整仓嵌入。
- **可用性：** 中低（预打包二进制，要求 Linux + bubblewrap）。

### 2.3 本项目基本用不上

| 仓库 | 作用 | 为何跳过 |
|------|------|----------|
| agent-core-java / agent-runtime-java | Java 对等实现 | 本项目走 Python + DeepSearch |
| agent-protocol | MCP / A2A 的 C++ SDK | 协议互操作，非研究能力 |
| agent-dx | Runtime 的分布式执行底座 | 依赖 runtime 规模化之后 |
| agent-tools | 推理路由、vLLM 亲和调度 | 不是搜索/研报工具箱 |
| jiuwensymbiosis | 具身 / Physical AI | 场景不符 |
| relay | 多 Agent 协作开发/Code Review | 研发协作，非科研简报 |
| CareerSim-BDCI26 | 2026 大赛赛题 | 无关 |
| docs / community / .github | 文档与治理 | 可读，不是运行依赖 |
| agent-gateway | GitCode 标明 Opening Soon | 尚未作为可用模块 |

GitCode 还提到 **agent-store**（智能体商店），GitHub 组织当前 19 仓列表中未见同名仓，暂不计入可依赖项。

---

## 3. 对本项目的可用性结论

```
现在就要用
  ├─ agent-core     骨架：Agent / Workflow / Tool / LLM
  └─ deepsearch     能力：规划-检索-精读-溯源-成稿

明确可复用、但推迟
  ├─ agent-runtime  给领导提供稳定 HTTP 服务时
  ├─ agent-studio   要可视化配知识库/模型时
  ├─ agent-memory   要记住领导偏好时
  ├─ jiuwenswarm    要 IM（飞书/企微）入口时
  └─ skillhub       要把口径做成可分发 Skill 时

只借鉴、不接入
  └─ sciencediscovery  文献/科研工作流参考，产品定位不同

不要用
  └─ Java 栈、具身、协议 C++、vLLM 调度、大赛仓、Opening Soon 网关
```

### 建议的依赖关系（修正后）

```
领导 Deep Research 业务层（本仓库）
        │  模板 / 意图槽位 / 面上口径 / 证据规则
        ▼
   deepsearch（开箱即用的研究引擎）
        │  基于
        ▼
   agent-core（openjiuwen SDK）
        │
        ├── LLM API（Qwen3-Max 等已验证模型）
        └── 可选后期：agent-runtime 发布  /  memory  /  Swarm 渠道
```

---

## 4. 对前期规划的修正

| 原规划假设 | 实际情况 |
|-----------|----------|
| 复用 agent-runtime 做多步 plan-act-observe | 多步执行在 **agent-core**；runtime 是部署平台 |
| 在 deepsearch 之上自建整条研究工作流 | DeepSearch **已经是**查询规划+多源检索+反思+带引用研报；应定制而非重写 |
| 三种模式（汇报/学习/立项）要全新实现 | 应对齐 DeepSearch 的「样例/模板生成报告」，把三种模式做成三套模板 |

---

## 5. 建议的下一步（Phase 0）

1. 锁定版本：`openjiuwen`（PyPI）+ `deepsearch` 某一 commit/tag  
2. 本机按 DeepSearch SDK 文档跑通一条「学术与政策研究」样例  
3. 对照 API：`run`、`conversation_id`、模板注入、引用结构  
4. 再在本仓库实现领导模板（brief / learn / proposal），而不是再造检索引擎  

来源：GitHub 组织 API、各仓 README、GitCode 架构总览、DeepSearch / Runtime / Core 官方说明。
