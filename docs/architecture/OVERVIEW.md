# Architecture Overview

TMB AI OS uses a modular, content-first architecture. Markdown is the canonical
content artifact. Providers, agents, renderers, workflows, knowledge retrieval,
and integrations are replaceable modules.

```text
API -> Content Engine -> Provider Factory -> AI Provider
                    -> Markdown Renderer -> Draft Storage
```

## Design rules

1. Business services must not import vendor SDKs directly.
2. Prompts must live outside Python source code.
3. AI output is content first; metadata is secondary.
4. Provider-specific errors are normalized before reaching the API layer.
5. New modules must remain testable without external API calls.
6. No customer-confidential data may be embedded in source code or prompts.
