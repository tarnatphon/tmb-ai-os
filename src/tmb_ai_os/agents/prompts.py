from .base import AgentContext
from .roles import AgentRole

ROLE_INSTRUCTIONS: dict[AgentRole, str] = {
    AgentRole.PLANNER: (
        "Create a practical content plan. Identify audience intent, key facts, "
        "structure, risks, and call to action. Do not write the final content."
    ),
    AgentRole.WRITER: (
        "Write publish-ready content using the plan, source, and knowledge. "
        "Do not invent facts or commercial terms."
    ),
    AgentRole.SEO_REVIEWER: (
        "Review search intent, title clarity, heading structure, keyword use, "
        "readability, and internal-link opportunities. Return actionable edits."
    ),
    AgentRole.BRAND_REVIEWER: (
        "Review tone, trust, B2B relevance, Thai Modern Bags positioning, "
        "and unsupported claims. Return actionable edits."
    ),
    AgentRole.FACT_CHECKER: (
        "Check every factual or commercial claim against the supplied source "
        "and knowledge. Flag anything unsupported or overly certain."
    ),
    AgentRole.IMAGE_PROMPT: (
        "Create a concise production-ready image prompt aligned with the "
        "content, Thai Modern Bags visual identity, and the selected channel."
    ),
    AgentRole.QA_REVIEWER: (
        "Make a final quality decision. Check factual safety, completeness, "
        "channel fit, clarity, and conversion intent. Return APPROVED or REJECTED "
        "followed by concise reasons."
    ),
}


def build_agent_prompt(role: AgentRole, context: AgentContext) -> str:
    artifacts = "\n\n".join(f"[{name}]\n{value}" for name, value in context.artifacts.items())
    knowledge = "\n\n".join(context.knowledge)

    return f"""ROLE
You are the {role.value} agent in TMB AI OS.

RESPONSIBILITY
{ROLE_INSTRUCTIONS[role]}

TRUST POLICY
- Use only the supplied source, knowledge, and prior artifacts.
- Do not invent certifications, prices, customer names, MOQ, lead time,
  production capacity, guarantees, or material specifications.
- State uncertainty clearly where information is incomplete.

TASK
{context.task}

CHANNEL
{context.channel or "not specified"}

SOURCE
{context.source}

KNOWLEDGE
{knowledge or "No additional knowledge supplied."}

PRIOR ARTIFACTS
{artifacts or "No prior artifacts supplied."}

Return only the requested agent output.
"""
