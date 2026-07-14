# Legacy Call-Site Migration

## Internal import policy

Internal code must import canonical modules directly:

```python
from tmb_ai_os.config import get_settings
from tmb_ai_os.provider_contracts import GenerationRequest
from tmb_ai_os.provider_factory import create_text_generator
```

Internal code must not import:

```python
from app.core.config import ...
from app.providers.base import ...
from app.providers.factory import ...
```

## Compatibility wrappers

The wrappers remain temporarily for:

- External integrations
- Older scripts
- Rollback safety

They may be removed only after the call-site guard remains clean for a complete
release cycle.
