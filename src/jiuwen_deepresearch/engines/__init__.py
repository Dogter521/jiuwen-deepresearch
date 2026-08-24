from __future__ import annotations

from typing import Protocol

from jiuwen_deepresearch.models import ResearchResult


class ResearchEngine(Protocol):
    name: str

    async def run(self, query: str, template: str, conversation_id: str) -> ResearchResult:
        ...
