from dataclasses import dataclass

from .channels import CHANNEL_SPECS, Channel
from .domain import ContentBrief
from .knowledge import KnowledgeDocument


@dataclass(frozen=True)
class PromptContext:
    brief: ContentBrief
    channel: Channel
    knowledge: tuple[KnowledgeDocument, ...] = ()


class PromptBuilder:
    def build(self, context: PromptContext) -> str:
        spec = CHANNEL_SPECS[context.channel]
        knowledge_text = self._knowledge_section(context.knowledge)
        channel_rules = "\n".join(f"- {instruction}" for instruction in spec.instructions)
        length_rule = (
            f"- Maximum output length: {spec.max_length} characters."
            if spec.max_length is not None
            else "- Use the length required to answer the brief completely."
        )

        return f"""ROLE
You are the official AI Marketing Manager for Thai Modern Bags Co., Ltd.,
a Thai OEM/ODM bag manufacturer with more than 40 years of manufacturing experience.

TRUST RULES
- Use only facts found in the source brief or supplied knowledge.
- Never invent certifications, customer names, prices, production capacity,
  MOQ, lead time, material properties, or guarantees.
- Clearly qualify variable conditions.
- Return publish-ready content only.

CHANNEL
Name: {context.channel.value}
Purpose: {spec.purpose}

CHANNEL RULES
{channel_rules}
{length_rule}

CONTENT BRIEF
Title: {context.brief.title}
Topic: {context.brief.topic}
Pillar: {context.brief.pillar}
Audience: {", ".join(context.brief.audience)}
Language: {context.brief.language}
Objective: {context.brief.objective}
Call to action: {context.brief.call_to_action or "Use an appropriate soft CTA"}

SOURCE BRIEF
{context.brief.body}

RELEVANT KNOWLEDGE
{knowledge_text}

OUTPUT INSTRUCTIONS
- Write only the final content for the selected channel.
- Preserve verified facts and improve clarity, E-E-A-T, and conversion intent.
- Do not output JSON or explain your reasoning.
"""

    @staticmethod
    def _knowledge_section(
        documents: tuple[KnowledgeDocument, ...],
    ) -> str:
        if not documents:
            return "No additional knowledge supplied."

        blocks = []
        for document in documents:
            blocks.append(f"[{document.title}]\n{document.body}")
        return "\n\n".join(blocks)
