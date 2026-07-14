from dataclasses import dataclass
from enum import StrEnum


class Channel(StrEnum):
    WEBSITE_BLOG = "website_blog"
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    X = "x"
    LINKEDIN = "linkedin"


@dataclass(frozen=True)
class ChannelSpec:
    name: Channel
    purpose: str
    max_length: int | None
    instructions: tuple[str, ...]


CHANNEL_SPECS: dict[Channel, ChannelSpec] = {
    Channel.WEBSITE_BLOG: ChannelSpec(
        name=Channel.WEBSITE_BLOG,
        purpose="Long-form educational and conversion-oriented website content",
        max_length=None,
        instructions=(
            "Use clear H2 and H3 headings.",
            "Include an informative introduction, practical detail, FAQ, and CTA.",
            "Use SEO naturally without keyword stuffing.",
        ),
    ),
    Channel.FACEBOOK: ChannelSpec(
        name=Channel.FACEBOOK,
        purpose="Helpful B2B social post that encourages enquiries",
        max_length=2200,
        instructions=(
            "Open with a strong practical hook.",
            "Use short paragraphs suitable for mobile reading.",
            "End with a clear but non-aggressive CTA.",
        ),
    ),
    Channel.INSTAGRAM: ChannelSpec(
        name=Channel.INSTAGRAM,
        purpose="Visual-first caption for business and product audiences",
        max_length=1800,
        instructions=(
            "Use a concise hook and scannable lines.",
            "Add relevant hashtags after the main caption.",
            "Do not overuse emojis.",
        ),
    ),
    Channel.X: ChannelSpec(
        name=Channel.X,
        purpose="Concise business insight suitable for X",
        max_length=280,
        instructions=(
            "Stay within 280 characters.",
            "Communicate one main idea.",
            "Avoid long hashtag lists.",
        ),
    ),
    Channel.LINKEDIN: ChannelSpec(
        name=Channel.LINKEDIN,
        purpose="Professional manufacturing and procurement insight",
        max_length=2200,
        instructions=(
            "Use a professional and authoritative tone.",
            "Highlight business value and manufacturing considerations.",
            "End with a discussion or enquiry prompt.",
        ),
    ),
}


def parse_channels(values: list[str]) -> list[Channel]:
    channels: list[Channel] = []
    for value in values:
        normalized = value.strip().lower()
        try:
            channel = Channel(normalized)
        except ValueError:
            continue
        if channel not in channels:
            channels.append(channel)
    return channels
