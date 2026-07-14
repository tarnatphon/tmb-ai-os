from tmb_ai_os.channels import Channel, parse_channels


def test_parse_channels_filters_unknown_and_duplicates() -> None:
    result = parse_channels(["facebook", "unknown", "facebook", "x"])

    assert result == [Channel.FACEBOOK, Channel.X]
