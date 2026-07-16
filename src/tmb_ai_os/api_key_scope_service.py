from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from .api_key_models import ManagedApiKey
from .api_key_scope_models import ManagedApiKeyScope
from .api_key_service import ApiKeyNotFoundError
from .scopes import ApiScope, default_scopes_for_role
from .security import Role


class ApiKeyScopeService:
    def get_scopes(
        self,
        session: Session,
        key_id: str,
    ) -> frozenset[ApiScope]:
        row = self._get_key(session, key_id)
        scopes = session.scalars(
            select(ManagedApiKeyScope.scope).where(ManagedApiKeyScope.api_key_id == row.id)
        ).all()

        if scopes:
            return frozenset(ApiScope(scope) for scope in scopes)

        return default_scopes_for_role(Role(row.role))

    def replace_scopes(
        self,
        session: Session,
        *,
        key_id: str,
        scopes: set[ApiScope],
    ) -> frozenset[ApiScope]:
        row = self._get_key(session, key_id)

        session.execute(delete(ManagedApiKeyScope).where(ManagedApiKeyScope.api_key_id == row.id))
        for scope in sorted(scopes, key=str):
            session.add(
                ManagedApiKeyScope(
                    api_key_id=row.id,
                    scope=scope.value,
                )
            )

        session.commit()
        return frozenset(scopes)

    @staticmethod
    def _get_key(
        session: Session,
        key_id: str,
    ) -> ManagedApiKey:
        row = session.scalar(select(ManagedApiKey).where(ManagedApiKey.key_id == key_id))
        if row is None:
            raise ApiKeyNotFoundError(f"API key not found: {key_id}")
        return row
