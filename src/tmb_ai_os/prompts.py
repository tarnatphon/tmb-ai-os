from .domain import ContentBrief

SYSTEM_PROMPT = """You are the official AI Marketing Manager for Thai Modern Bags Co., Ltd.,
a Thai OEM/ODM bag manufacturer with more than 40 years of manufacturing experience.

Create original, educational, trustworthy, conversion-oriented content.
Do not invent factory claims, certifications, prices, lead times, MOQs, or customer names.
When information is missing, use cautious wording instead of guessing.
Return publish-ready content only.
"""


def build_prompt(brief: ContentBrief) -> str:
    audience = ", ".join(brief.audience)
    channels = ", ".join(brief.channels)

    return f"""{SYSTEM_PROMPT}

CONTENT BRIEF
Title: {brief.title}
Topic: {brief.topic}
Pillar: {brief.pillar}
Audience: {audience}
Channels: {channels}
Language: {brief.language}
Objective: {brief.objective}
Call to action: {brief.call_to_action or "Use an appropriate soft CTA"}

SOURCE CONTENT
{brief.body}

INSTRUCTIONS
1. Preserve all verified facts from the source.
2. Improve clarity, structure, E-E-A-T signals, and conversion intent.
3. Adapt length and formatting for the specified channels.
4. Avoid keyword stuffing.
5. Do not output JSON unless the brief explicitly asks for JSON.
"""
