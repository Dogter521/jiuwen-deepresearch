from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Goal = Literal["brief", "learn", "proposal"]
Depth = Literal["L1", "L2", "L3"]
Horizon = Literal["6m", "1-3y", "5y+"]
Confidence = Literal["high", "medium", "low"]
Layer = Literal["academic", "industry", "policy", "unknown"]
EvidenceStatus = Literal["consensus", "dispute", "unknown"]


class Intent(BaseModel):
    goal: Goal = "brief"
    topic: str
    horizon: Horizon = "1-3y"
    audience: str = "院所领导"
    constraints: str = ""
    depth: Depth = "L1"
    raw_query: str = ""

    @property
    def mode_label(self) -> str:
        return {"brief": "汇报", "learn": "学习", "proposal": "立项"}[self.goal]


class EvidenceItem(BaseModel):
    claim: str
    source_title: str = ""
    source_url: str = ""
    layer: Layer = "unknown"
    confidence: Confidence = "low"
    status: EvidenceStatus = "unknown"


class ResearchResult(BaseModel):
    markdown: str
    conversation_id: str
    engine: str
    sources: list[EvidenceItem] = Field(default_factory=list)
    events: list[str] = Field(default_factory=list)
    used_template: str = ""
