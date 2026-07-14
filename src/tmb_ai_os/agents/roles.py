from enum import StrEnum


class AgentRole(StrEnum):
    PLANNER = "planner"
    WRITER = "writer"
    SEO_REVIEWER = "seo_reviewer"
    BRAND_REVIEWER = "brand_reviewer"
    FACT_CHECKER = "fact_checker"
    IMAGE_PROMPT = "image_prompt"
    QA_REVIEWER = "qa_reviewer"
