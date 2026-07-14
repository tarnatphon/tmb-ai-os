from pathlib import Path

from tmb_ai_os.migration.callsites import find_legacy_callsites


def main() -> None:
    findings = find_legacy_callsites(Path.cwd())

    if not findings:
        print("Legacy call-site check passed")
        return

    print("Legacy call-site check failed")
    for finding in findings:
        relative = finding.file.relative_to(Path.cwd())
        print(f"- {relative}:{finding.line}: {finding.legacy_module}")

    raise SystemExit(1)


if __name__ == "__main__":
    main()
