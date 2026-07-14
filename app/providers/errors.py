class ProviderError(RuntimeError):
    """Base error exposed by AI providers."""


class ProviderConfigurationError(ProviderError):
    pass


class ProviderUnavailableError(ProviderError):
    pass


class ProviderQuotaError(ProviderError):
    pass
