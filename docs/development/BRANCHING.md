# Branching Strategy

- `main`: releasable production history
- `develop`: integration branch for the next release
- `feature/*`: new capabilities
- `fix/*`: non-emergency fixes
- `hotfix/*`: urgent production fixes
- `release/*`: stabilization before a release

Pull requests target `develop` unless they are a release or hotfix.
