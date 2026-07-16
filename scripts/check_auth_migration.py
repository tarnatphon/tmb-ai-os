import ast
from pathlib import Path

FILES = (
    Path("src/tmb_ai_os/api_v18.py"),
    Path("src/tmb_ai_os/api_v19.py"),
)


def call_name(node: ast.Call) -> str | None:
    if isinstance(node.func, ast.Name):
        return node.func.id

    if isinstance(node.func, ast.Attribute):
        return node.func.attr

    return None


def main() -> None:
    failures: list[str] = []

    for path in FILES:
        text = path.read_text(encoding="utf-8")

        try:
            tree = ast.parse(text, filename=str(path))
        except SyntaxError as exc:
            failures.append(f"Unable to parse {path}: {exc}")
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and call_name(node) == "permission_dependency":
                failures.append(
                    f"Legacy permission dependency remains in "
                    f"{path}:{node.lineno}"
                )

    if failures:
        raise SystemExit("\n".join(failures))

    print("Authentication migration check passed")


if __name__ == "__main__":
    main()
