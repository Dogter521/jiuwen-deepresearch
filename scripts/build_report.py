#!/usr/bin/env python3
"""Generate the openJiuwen Deep Research planning report PDF."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    ListFlowable,
    ListItem,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "面向领导的AI知识DeepResearch建设报告.pdf"
SONGTI = "/System/Library/Fonts/Supplemental/Songti.ttc"

NAVY = HexColor("#0F2744")
NAVY2 = HexColor("#1B3A5F")
GOLD = HexColor("#C4A35A")
INK = HexColor("#1C2430")
MUTED = HexColor("#5B6775")
LINE = HexColor("#D5DCE3")
ROW = HexColor("#F4F7FA")
CALL = HexColor("#F7F1E4")
PALE = HexColor("#EEF3F8")


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("Song", SONGTI, subfontIndex=0))
    pdfmetrics.registerFont(TTFont("SongBd", SONGTI, subfontIndex=2))


def styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    s: dict[str, ParagraphStyle] = {}
    s["h1"] = ParagraphStyle(
        "h1",
        parent=base["Normal"],
        fontName="SongBd",
        fontSize=16,
        leading=24,
        textColor=NAVY,
        spaceBefore=14,
        spaceAfter=8,
        wordWrap="CJK",
    )
    s["h2"] = ParagraphStyle(
        "h2",
        parent=base["Normal"],
        fontName="SongBd",
        fontSize=12.5,
        leading=20,
        textColor=NAVY2,
        spaceBefore=10,
        spaceAfter=6,
        wordWrap="CJK",
    )
    s["h3"] = ParagraphStyle(
        "h3",
        parent=base["Normal"],
        fontName="SongBd",
        fontSize=11,
        leading=17,
        textColor=INK,
        spaceBefore=8,
        spaceAfter=4,
        wordWrap="CJK",
    )
    s["body"] = ParagraphStyle(
        "body",
        parent=base["Normal"],
        fontName="Song",
        fontSize=10,
        leading=16.5,
        textColor=INK,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
        wordWrap="CJK",
        firstLineIndent=0,
    )
    s["bullet"] = ParagraphStyle(
        "bullet",
        parent=s["body"],
        leftIndent=12,
        spaceAfter=3,
        alignment=TA_LEFT,
    )
    s["cell"] = ParagraphStyle(
        "cell",
        parent=base["Normal"],
        fontName="Song",
        fontSize=8.2,
        leading=12.5,
        textColor=INK,
        wordWrap="CJK",
    )
    s["cellb"] = ParagraphStyle(
        "cellb",
        parent=s["cell"],
        fontName="SongBd",
        textColor=white,
        alignment=TA_CENTER,
    )
    s["cellc"] = ParagraphStyle(
        "cellc",
        parent=s["cell"],
        alignment=TA_CENTER,
    )
    s["call"] = ParagraphStyle(
        "call",
        parent=s["body"],
        fontSize=9.5,
        leading=15.5,
        textColor=INK,
        alignment=TA_LEFT,
    )
    s["cover_kicker"] = ParagraphStyle(
        "cover_kicker",
        parent=base["Normal"],
        fontName="Song",
        fontSize=11,
        leading=16,
        textColor=GOLD,
        alignment=TA_LEFT,
        wordWrap="CJK",
    )
    s["cover_title"] = ParagraphStyle(
        "cover_title",
        parent=base["Normal"],
        fontName="SongBd",
        fontSize=26,
        leading=38,
        textColor=white,
        alignment=TA_LEFT,
        wordWrap="CJK",
    )
    s["cover_sub"] = ParagraphStyle(
        "cover_sub",
        parent=base["Normal"],
        fontName="Song",
        fontSize=13,
        leading=22,
        textColor=HexColor("#D9E4F0"),
        alignment=TA_LEFT,
        wordWrap="CJK",
    )
    s["cover_meta"] = ParagraphStyle(
        "cover_meta",
        parent=base["Normal"],
        fontName="Song",
        fontSize=10,
        leading=18,
        textColor=HexColor("#C5D0DC"),
        wordWrap="CJK",
    )
    s["footer"] = ParagraphStyle(
        "footer",
        parent=base["Normal"],
        fontName="Song",
        fontSize=8,
        textColor=MUTED,
        wordWrap="CJK",
    )
    s["toc"] = ParagraphStyle(
        "toc",
        parent=s["body"],
        fontSize=11,
        leading=20,
        alignment=TA_LEFT,
    )
    s["cap"] = ParagraphStyle(
        "cap",
        parent=s["body"],
        fontSize=8.5,
        leading=13,
        textColor=MUTED,
        alignment=TA_CENTER,
        spaceBefore=2,
        spaceAfter=8,
    )
    return s


def p(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(text.replace("\n", "<br/>"), style)


def th(text: str, st: dict) -> Paragraph:
    return p(text, st["cellb"])


def td(text: str, st: dict, center: bool = False) -> Paragraph:
    return p(text, st["cellc"] if center else st["cell"])


def make_table(headers: list[str], rows: list[list[str]], widths: list[float], st: dict) -> Table:
    data = [[th(h, st) for h in headers]]
    for row in rows:
        data.append([td(c, st, center=(i == len(row) - 1 and False)) for i, c in enumerate(row)])
    # rebuild with mixed center only when requested via trailing None
    data = [[th(h, st) for h in headers]]
    for row in rows:
        data.append([td(c, st) for c in row])
    tbl = Table(data, colWidths=widths, repeatRows=1)
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "SongBd"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("GRID", (0, 0), (-1, -1), 0.3, LINE),
        ("BACKGROUND", (0, 1), (-1, -1), white),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            cmds.append(("BACKGROUND", (0, i), (-1, i), ROW))
    tbl.setStyle(TableStyle(cmds))
    return tbl


def callout(text: str, st: dict, width: float) -> Table:
    inner = Table([[p(text, st["call"])]], colWidths=[width - 8 * mm])
    inner.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), CALL),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LINEBEFORE", (0, 0), (0, -1), 3, GOLD),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return inner


def draw_cover(canvas, doc) -> None:
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, w, h, fill=1, stroke=0)
    canvas.setFillColor(NAVY2)
    canvas.rect(0, 0, 18 * mm, h, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(18 * mm, 0, 2.2 * mm, h, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(28 * mm, h - 42 * mm, 28 * mm, 1.4, fill=1, stroke=0)
    canvas.setFillColor(HexColor("#0A1C33"))
    canvas.rect(0, 0, w, 28 * mm, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(0, 28 * mm, w, 0.8, fill=1, stroke=0)
    canvas.setFillColor(HexColor("#9AA8B8"))
    canvas.setFont("Song", 8.5)
    canvas.drawString(28 * mm, 14 * mm, "内部规划材料  |  基于公开仓库调研  |  不作为最终学术判断")
    canvas.restoreState()


def draw_page(canvas, doc) -> None:
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(NAVY)
    canvas.rect(0, h - 12 * mm, w, 12 * mm, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(0, h - 12.7 * mm, w, 0.7, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont("Song", 8)
    canvas.drawString(18 * mm, h - 8 * mm, "jiuwen-deepresearch  |  面向领导的 AI 知识 Deep Research Agent")
    canvas.drawRightString(w - 18 * mm, h - 8 * mm, "建设规划报告 v1.0")
    canvas.setFillColor(LINE)
    canvas.rect(18 * mm, 14 * mm, w - 36 * mm, 0.4, fill=1, stroke=0)
    canvas.setFillColor(MUTED)
    canvas.setFont("Song", 8)
    canvas.drawString(18 * mm, 8 * mm, "2026-08-20")
    canvas.drawRightString(w - 18 * mm, 8 * mm, f"- {doc.page - 1} -")
    canvas.restoreState()


def bullets(items: list[str], st: dict) -> list:
    out = []
    for t in items:
        out.append(p("· " + t, st["bullet"]))
    return out


def build() -> None:
    register_fonts()
    st = styles()
    OUT.parent.mkdir(parents=True, exist_ok=True)

    W = A4[0] - 36 * mm

    doc = BaseDocTemplate(
        str(OUT),
        pagesize=A4,
        title="面向领导的AI知识Deep Research建设规划报告",
        author="jiuwen-deepresearch",
    )
    cover_frame = Frame(28 * mm, 40 * mm, A4[0] - 48 * mm, A4[1] - 90 * mm, id="cover")
    body_frame = Frame(18 * mm, 20 * mm, W, A4[1] - 38 * mm, id="body")
    doc.addPageTemplates(
        [
            PageTemplate(id="cover", frames=[cover_frame], onPage=draw_cover),
            PageTemplate(id="body", frames=[body_frame], onPage=draw_page),
        ]
    )

    story = []

    # Cover
    story.append(p("openJiuwen 开源调研  ·  项目建设规划", st["cover_kicker"]))
    story.append(Spacer(1, 10 * mm))
    story.append(p("面向领导的 AI 知识<br/>Deep Research Agent", st["cover_title"]))
    story.append(Spacer(1, 6 * mm))
    story.append(p("开源能力复用分析、仓库可用性评估与实施路线", st["cover_sub"]))
    story.append(Spacer(1, 16 * mm))
    story.append(
        p(
            "项目目录：jiuwen-deepresearch<br/>"
            "调研对象：github.com/openJiuwen-ai（19 个公开仓）<br/>"
            "日期：2026 年 8 月 20 日<br/>"
            "版本：v1.0  |  状态：调研完成，待进入 Phase 0",
            st["cover_meta"],
        )
    )
    story.append(NextPageTemplate("body"))
    story.append(PageBreak())

    # TOC
    story.append(p("目录", st["h1"]))
    toc = [
        "一、摘要与核心结论",
        "二、项目定位与验收标准",
        "三、openJiuwen 生态调研",
        "四、仓库可用性评估",
        "五、建设策略与目标架构",
        "六、产品形态与研究工作流",
        "七、实施路线、风险与待决策",
        "附录  十九仓一览与资料来源",
    ]
    for t in toc:
        story.append(p(t, st["toc"]))
    story.append(Spacer(1, 8 * mm))
    story.append(
        callout(
            "<b>阅读指引：</b>第 1 节给出可用性总表，可单独传阅；"
            "第 3–4 节是对 github.com/openJiuwen-ai 十九个公开仓的调研；"
            "第 5–7 节是修正后的架构、产品形态与实施路线。"
            "核心判断：现在复用 agent-core 与 deepsearch，MVP 不上 agent-runtime。",
            st,
            W,
        )
    )
    story.append(PageBreak())

    # 1
    story.append(p("一、摘要与核心结论", st["h1"]))
    story.append(
        p(
            "本项目要做的不是再写一篇学术综述，而是一个给领导用的深度研究 Agent："
            "把 AI 知识与面上科研收成「能拍板」的简报——一句话结论、一页要点、证据链、风险与 30/90 天动作。",
            st["body"],
        )
    )
    story.append(
        callout(
            "<b>一句话策略：</b>在 DeepSearch 之上做薄业务层（领导三种模板、意图槽位、证据口径），"
            "复用 agent-core 作为骨架。不要重写检索-规划-成稿链路，也不要把 agent-runtime 当成执行引擎。",
            st,
            W,
        )
    )
    story.append(Spacer(1, 4 * mm))
    story.append(p("对 19 个公开仓的可用性结论", st["h2"]))
    story.append(
        make_table(
            ["优先级", "仓库", "用途"],
            [
                ["现在就要用", "agent-core", "SDK 骨架：Agent / 工作流 / 工具 / LLM，自带进程内执行引擎"],
                ["现在就要用", "deepsearch", "深度研究引擎：规划、检索、反思、片段引用、模板研报"],
                ["第二期再接", "agent-runtime", "生产部署与生命周期；对外提供 HTTP 服务时再用"],
                ["第二期再接", "studio / memory / swarm / skillhub", "可视化运营、长期记忆、IM 渠道、Skill 分发"],
                ["只借鉴", "sciencediscovery", "科研实验工作站，定位向下做实验，不宜整仓接入"],
                ["跳过", "Java 双栈、协议 C++、具身、大赛仓等", "与本项目目标无关"],
            ],
            [28 * mm, 42 * mm, W - 70 * mm],
            st,
        )
    )
    story.append(p("表 1  对本项目的可用性总表", st["cap"]))

    # 2
    story.append(p("二、项目定位与验收标准", st["h1"]))
    story.append(p("2.1 要解决什么", st["h2"]))
    story.append(
        make_table(
            ["领导问法", "Agent 应交付的形态"],
            [
                ["AI 现在到哪一步了？", "技术成熟度地图 + 可信度标注"],
                ["我们该投什么方向？", "机会窗口 / 风险 / 竞品与政策约束"],
                ["某领域论文或项目在说什么？", "三层摘要：一句话 → 一页简报 → 证据链"],
                ["面上科研怎么布局？", "问题树、关键路径、资源与人才缺口"],
            ],
            [58 * mm, W - 58 * mm],
            st,
        )
    )
    story.append(p("表 2  问题与交付形态", st["cap"]))
    story.append(p("「面上科研」统一口径（建议）", st["h3"]))
    story.extend(
        bullets(
            [
                "面向上层决策的科研认知：趋势、格局、瓶颈、可落地路径。",
                "可映射到基金 / 规划语境：问题提出、研究意义、技术路线、预期成果。",
                "刻意控制深度：默认到「能拍板」，按需下钻到「能答辩」。",
            ],
            st,
        )
    )
    story.append(p("2.2 非目标与验收", st["h2"]))
    story.append(
        p(
            "不做：替代专家终审、无引用胡编、一次输出几十页长文、第一期与业务系统深度耦合。"
            "验收：典型问题能产出领导简报 + 证据清单 + 追问入口；结论可回溯来源；支持多轮收窄 / 加深 / 对比 / 改写；"
            "架构上可见地复用 openJiuwen。",
            st["body"],
        )
    )

    # 3
    story.append(p("三、openJiuwen 生态调研", st["h1"]))
    story.append(
        p(
            "openJiuwen 是分层 Agent 平台，不是单一框架。组织地址 github.com/openJiuwen-ai，"
            "国内镜像 gitcode.com/openJiuwen，站点 openjiuwen.com。调研当日 GitHub 公开仓 19 个。",
            st["body"],
        )
    )
    story.append(
        make_table(
            ["层", "作用", "代表仓库"],
            [
                ["Deep Agents", "面向场景的成品智能体", "deepsearch、jiuwenswarm、sciencediscovery"],
                ["Agent Studio", "低码可视化开发与资源管理", "agent-studio"],
                ["Framework", "SDK、记忆、协议", "agent-core、agent-memory、agent-protocol"],
                ["Runtime", "从开发态到生产态", "agent-runtime、agent-dx"],
                ["生态治理", "Skill 分发、文档、社区", "skillhub、docs、community"],
            ],
            [32 * mm, 58 * mm, W - 90 * mm],
            st,
        )
    )
    story.append(p("表 3  openJiuwen 分层与代表仓", st["cap"]))
    story.append(
        callout(
            "<b>关键纠正：</b>agent-core 已包含进程内执行引擎（图执行、ReAct / Workflow、流式、中断恢复）。"
            "agent-runtime 是服务化部署平台（subprocess / Docker / K8s、REST 发布、多租户），"
            "不是「多步思考发动机」。Deep Research 的多步循环应落在 agent-core + deepsearch。",
            st,
            W,
        )
    )
    story.append(Spacer(1, 3 * mm))

    # 4
    story.append(p("四、仓库可用性评估", st["h1"]))
    story.append(p("4.1 现在就要用", st["h2"]))
    story.append(p("agent-core（Python，GitHub ★426，Apache-2.0）", st["h3"]))
    story.append(
        p(
            "官方核心 SDK，PyPI 包名 openjiuwen，安装命令 pip install -U openjiuwen。"
            "环境要求 Python ≥3.11 且 &lt;3.14，推荐 3.11.4。提供 ReActAgent、WorkflowAgent、工具调用、"
            "异步图执行、流式与 checkpoint。DeepSearch 基于它构建。本项目的 Agent / Tool / 会话都应挂在这层。"
            "可用性：高，有 PyPI 与持续推送，默认分支 develop。",
            st["body"],
        )
    )
    story.append(p("deepsearch（Python，GitHub ★115）", st["h3"]))
    story.append(
        p(
            "知识增强深度检索与研究引擎，流程为查询规划 → 信息收集 → 理解反思 → 报告生成。"
            "卖点包括片段级引用、溯源推理、按样例 / 模板生成研报，以及本地知识库与网页融合检索。"
            "官方场景已覆盖金融研报、学术与政策研究，与「领导面上科研」高度同构。"
            "仓内另含 codesearch 与 base；近期合入目标论文精确识别与引用传递。"
            "已验证模型：Qwen3-Max（推荐）、GLM-5 / 5.1、DeepSeek V3.2、Kimi-K2.5。"
            "注意：除 HITL / 终止外，SDK run 每次需不同 conversation_id；GitHub license 元数据为空，落地前核对 LICENSE。",
            st["body"],
        )
    )
    story.append(
        callout(
            "<b>结论：</b>deepsearch 是首选复用对象。我们实现领导口径模板与来源分层策略，挂在其报告生成层之上，不重写引擎。",
            st,
            W,
        )
    )
    story.append(Spacer(1, 3 * mm))
    story.append(p("4.2 第二期再接", st["h2"]))
    story.append(
        make_table(
            ["仓库", "作用", "何时接入", "可用性"],
            [
                ["agent-runtime ★12", "部署、会话、生命周期；管理口默认 8186", "对外提供稳定 HTTP 服务时", "中；K8s 仍在完善"],
                ["agent-studio ★152", "低码配模型、知识库、工作流", "需要运营配置界面时", "中高，栈较重"],
                ["agent-memory ★51", "长期记忆 JiuwenMemory", "记住领导偏好与禁忌词时", "高，有 PyPI"],
                ["jiuwenswarm ★3167", "多 Agent + 飞书 / 企微等通道", "领导要在 IM 提问时作渠道层", "最高"],
                ["skillhub ★24", "Skill 托管分发", "口径要内部分发时", "中"],
            ],
            [38 * mm, 48 * mm, 48 * mm, W - 134 * mm],
            st,
        )
    )
    story.append(p("表 4  推迟接入的仓库", st["cap"]))
    story.append(p("4.3 只借鉴与跳过", st["h2"]))
    story.append(
        p(
            "sciencediscovery（★39）是科研工作站：文献、假设、写代码、沙箱实验、调参。"
            "面向研究者「往下做实验」，本项目面向领导「往上做决策」，不宜整仓嵌入；文献 Connector 以后可参考。"
            "运行依赖 Linux + bubblewrap，不是 macOS 桌面默认路径。",
            st["body"],
        )
    )
    story.append(
        p(
            "跳过：agent-core-java 与 agent-runtime-java（本项目走 Python）；agent-protocol（MCP/A2A 的 C++ SDK）；"
            "agent-dx（Runtime 分布式执行底座）；agent-tools（vLLM 推理路由，不是搜索工具箱）；"
            "jiuwensymbiosis（具身）；relay（协作开发）；CareerSim-BDCI26（大赛）；"
            "docs / community / .github（治理材料）；agent-gateway（Opening Soon）。"
            "GitCode 提到的 agent-store 在 GitHub 当前列表中未见，暂不计入依赖。",
            st["body"],
        )
    )

    # 5
    story.append(p("五、建设策略与目标架构", st["h1"]))
    story.append(p("5.1 相对初版规划的修正", st["h2"]))
    story.append(
        make_table(
            ["初版假设", "调研后的实际情况"],
            [
                ["用 agent-runtime 做多步 plan-act-observe", "多步执行在 agent-core；runtime 是部署平台"],
                ["在 deepsearch 之上自建整条研究工作流", "DeepSearch 已具备规划-检索-反思-带引用成稿，应定制而非重写"],
                ["三种模式要全新实现", "对齐其「按模板 / 样例生成报告」，做成三套模板即可"],
            ],
            [72 * mm, W - 72 * mm],
            st,
        )
    )
    story.append(p("表 5  规划修正对照", st["cap"]))
    arch = [
        ["领导业务层（本仓库）", "意图槽位、三种模板、面上口径、证据规则"],
        ["↓", ""],
        ["deepsearch", "开箱即用的研究引擎"],
        ["↓", ""],
        ["agent-core / openjiuwen", "Agent、工具、LLM、图执行"],
        ["↓", ""],
        ["LLM API 与后期可选件", "优先 Qwen3-Max 等已验证模型；后期 runtime / memory / Swarm 渠道"],
    ]
    arch_data = [[td(a, st), td(b, st)] for a, b in arch]
    arch_tbl = Table(arch_data, colWidths=[58 * mm, W - 58 * mm])
    arch_tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), PALE),
                ("BACKGROUND", (0, 2), (-1, 2), PALE),
                ("BACKGROUND", (0, 4), (-1, 4), PALE),
                ("BACKGROUND", (0, 6), (-1, 6), PALE),
                ("FONTNAME", (0, 0), (0, -1), "SongBd"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("BOX", (0, 0), (-1, -1), 0.6, NAVY2),
                ("LINEBELOW", (0, 0), (-1, -2), 0.3, LINE),
                ("ALIGN", (0, 1), (0, 1), "CENTER"),
                ("ALIGN", (0, 3), (0, 3), "CENTER"),
                ("ALIGN", (0, 5), (0, 5), "CENTER"),
            ]
        )
    )
    story.append(
        KeepTogether(
            [
                p("5.2 建议架构", st["h2"]),
                arch_tbl,
                p("图 1  依赖关系（调研后）", st["cap"]),
                p(
                    "原则：业务逻辑放在本仓库薄层，执行与检索跟随上游升级。MVP 不上 agent-runtime，本地脚本或 CLI 调用即可。",
                    st["body"],
                ),
            ]
        )
    )

    # 6
    story.append(p("六、产品形态与研究工作流", st["h1"]))
    story.append(p("6.1 用户与三种模式", st["h2"]))
    story.append(
        p(
            "一级用户是领导 / 决策者，要短、要结论、要风险、要下一步；"
            "二级是秘书 / 战略研究岗，要可编辑稿、出处与对比表；"
            "三级是技术顾问，要可下钻证据链、方法与局限。",
            st["body"],
        )
    )
    story.append(
        make_table(
            ["模式", "目标", "输出偏重"],
            [
                ["汇报", "开会用", "1 页简报 + 3 条建议 + 风险"],
                ["学习", "补齐认知", "概念阶梯 + 类比 + 必读清单"],
                ["立项 / 面上", "写意义与路线", "问题提出 → 意义 → 路线 → 指标 → 风险"],
            ],
            [32 * mm, 32 * mm, W - 64 * mm],
            st,
        )
    )
    story.append(p("表 6  三种预设模式（做成 DeepSearch 模板）", st["cap"]))
    story.append(
        p(
            "固定章节：一句话结论；背景与为何现在重要；技术 / 产业 / 政策三棱镜；"
            "关键判断（带置信度）；风险与误区；建议动作（30 天 / 90 天）；附录来源与术语表。",
            st["body"],
        )
    )
    story.append(p("6.2 工作流（复用 DeepSearch，叠加领导策略）", st["h2"]))
    story.extend(
        bullets(
            [
                "意图澄清：决策 / 学习 / 立项；时间范围；深度 L1 简报 / L2 标准 / L3 深潜。",
                "查询规划：拆成技术、产业、政策、竞品、风险子问题；生成中英检索词。",
                "DeepSearch 广搜与融合检索。",
                "来源分层配额：学术 / 产业 / 政策每层保底，避免单一信源偏见。",
                "精读抽取：主张、证据、反证、适用边界。",
                "交叉验证：标注共识 / 争议 / 未知。",
                "按所选模板成稿并改写口径。",
                "多轮修订：更短、更偏产业、对比、改成口播。",
            ],
            st,
        )
    )
    story.append(
        p(
            "证据规则：无来源不得写事实断言；置信度高 / 中 / 低须显式标注；冲突必须呈现，不得静默择一。",
            st["body"],
        )
    )

    # 7
    story.append(p("七、实施路线、风险与待决策", st["h1"]))
    story.append(p("7.1 分阶段实施", st["h2"]))
    story.append(
        make_table(
            ["阶段", "周期", "主要工作"],
            [
                ["Phase 0 摸底", "0.5–1 天", "锁定 openjiuwen 与 deepsearch 版本；跑通学术 / 政策样例；整理 API 对照"],
                ["Phase 1 MVP", "3–5 天", "意图槽位 + 三套模板；打通澄清到成稿；Markdown 简报；5 条黄金问题验收"],
                ["Phase 2 强化", "约 1 周", "来源配额、冲突与置信度、精读预算、进度展示、面上立项改写"],
                ["Phase 3 可信", "持续", "评测集扩展、PPT 大纲导出、可选内网知识库"],
            ],
            [32 * mm, 28 * mm, W - 60 * mm],
            st,
        )
    )
    story.append(p("表 7  实施路线", st["cap"]))
    story.append(p("7.2 风险", st["h2"]))
    story.append(
        make_table(
            ["风险", "对策"],
            [
                ["检索噪声导致简报误导", "权威源分层配额 + 冲突展示"],
                ["模型幻觉、领导信任崩塌", "强制引用；无证据标「未知」"],
                ["时延过长", "先出 L1 快报，后台继续 L2"],
                ["上游 API 变动", "业务层只依赖薄适配器"],
                ["「面上」口径歧义", "以本报告第 2.1 节为准，产品评审确认"],
            ],
            [58 * mm, W - 58 * mm],
            st,
        )
    )
    story.append(p("表 8  主要风险与对策", st["cap"]))
    story.append(p("7.3 需要拍板的事项", st["h2"]))
    story.extend(
        bullets(
            [
                "部署形态：本地 CLI 优先，还是要 Web？",
                "模型：云端 API 还是本地 / 专有？是否必须国产化？",
                "「面上科研」以决策简报为主，还是要贴近基金申请书结构？",
                "检索是否必须覆盖 arXiv / CNKI / 政策库？有无内网资料？",
                "版本锁定：pin 到哪一个 release / commit？",
            ],
            st,
        )
    )
    story.append(p("7.4 建议的下一步", st["h2"]))
    story.extend(
        bullets(
            [
                "确认上述决策项（尤其是口径与检索范围）。",
                "进入 Phase 0：安装 agent-core 与 deepsearch，跑通官方样例。",
                "在本仓库落地三套领导模板，用 1–2 个真实领导问题打通全链路。",
            ],
            st,
        )
    )

    # Appendix
    story.append(p("附录  十九仓一览与资料来源", st["h1"]))
    story.append(p("A. GitHub 公开仓（2026-08-20 星标快照）", st["h2"]))
    story.append(
        make_table(
            ["仓库", "语言", "星标", "本项目态度"],
            [
                ["jiuwenswarm", "Python", "3167", "第二期渠道"],
                ["agent-core", "Python", "426", "现在用"],
                ["agent-studio", "Java", "152", "第二期可选"],
                ["deepsearch", "Python", "115", "现在用"],
                ["agent-protocol", "C++", "79", "跳过"],
                ["jiuwensymbiosis", "Python", "52", "跳过"],
                ["agent-memory", "Python", "51", "第二期可选"],
                ["sciencediscovery", "TypeScript", "39", "只借鉴"],
                ["agent-core-java", "Java", "31", "跳过"],
                ["docs", "Markdown", "30", "参考文档"],
                ["skillhub", "Python", "24", "第二期可选"],
                ["agent-runtime-java", "Java", "23", "跳过"],
                ["agent-tools", "Python", "17", "跳过"],
                ["community / agent-runtime", "— / Python", "12 / 12", "治理 / 服务化时再用"],
                ["CareerSim-BDCI26 / relay / .github / agent-dx", "杂", "5 / 4 / 3 / 0", "跳过"],
            ],
            [58 * mm, 28 * mm, 22 * mm, W - 108 * mm],
            st,
        )
    )
    story.append(p("表 9  仓库清单", st["cap"]))
    story.append(p("B. 资料来源", st["h2"]))
    story.extend(
        bullets(
            [
                "GitHub 组织页与 REST API：github.com/openJiuwen-ai",
                "GitCode 组织总览与各仓 README：gitcode.com/openJiuwen",
                "官方站点：www.openjiuwen.com",
                "agent-core、deepsearch、agent-runtime、agent-studio、agent-memory、jiuwenswarm、skillhub、sciencediscovery 各仓 README（调研当日）",
            ],
            st,
        )
    )
    story.append(Spacer(1, 8 * mm))
    story.append(
        callout(
            "本报告仅基于公开仓库与官方文档整理，用于项目内部规划。模型接入与具体业务场景的合规义务由使用方自行承担。",
            st,
            W,
        )
    )

    doc.build(story)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    build()
