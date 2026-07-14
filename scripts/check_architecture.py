from pathlib import Path

from tmb_ai_os.architecture import inspect_architecture


def main() -> None:
    report = inspect_architecture(Path.cwd())

    print(f"Canonical package: {report.canonical_package}")
    print(f"Legacy package: {report.legacy_package}")
    print(f"Canonical exists: {report.canonical_exists}")
    print(f"Legacy exists: {report.legacy_exists}")

    if report.duplicate_modules:
        print("Potential duplicate module names:")
        for name in report.duplicate_modules:
            print(f"- {name}")
    else:
        print("No duplicate module names found")


if __name__ == "__main__":
    main()
