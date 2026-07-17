from dataclasses import dataclass

from fastapi import FastAPI

from .security_policies import required_scope_for_route


@dataclass(frozen=True)
class PolicyGap:
    method: str
    path: str


@dataclass(frozen=True)
class PolicyComplianceReport:
    protected_routes: int
    covered_routes: int
    gaps: tuple[PolicyGap, ...]


PROTECTED_PREFIXES = (
    "/v18/dashboard",
    "/v16/incidents",
    "/v17/incidents",
    "/v20/api-keys",
    "/v22",
    "/v23/security",
)


def build_policy_compliance_report(
    app: FastAPI,
) -> PolicyComplianceReport:
    protected = 0
    covered = 0
    gaps: list[PolicyGap] = []

    for route in app.routes:
        path = getattr(route, "path", None)
        methods = getattr(route, "methods", None)

        if not path or not methods:
            continue
        if not path.startswith(PROTECTED_PREFIXES):
            continue

        for method in sorted(methods):
            if method in {"HEAD", "OPTIONS"}:
                continue
            protected += 1
            if (
                required_scope_for_route(
                    method=method,
                    path=path,
                )
                is None
            ):
                gaps.append(PolicyGap(method=method, path=path))
            else:
                covered += 1

    return PolicyComplianceReport(
        protected_routes=protected,
        covered_routes=covered,
        gaps=tuple(gaps),
    )
