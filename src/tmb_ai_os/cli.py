from pathlib import Path

import typer

from .config import get_settings
from .content import ContentRepository
from .prompts import build_prompt
from .providers import GeminiGenerator
from .service import ContentGenerationService

app = typer.Typer(no_args_is_help=True)


@app.command()
def validate() -> None:
    settings = get_settings()
    repository = ContentRepository(settings.content_dir)
    files = repository.list_markdown()

    if not files:
        typer.echo("No Markdown files found", err=True)
        raise typer.Exit(code=1)

    failed = 0
    for path in files:
        try:
            repository.load_brief(path)
            typer.echo(f"OK  {path}")
        except Exception as exc:
            failed += 1
            typer.echo(f"ERR {path}: {exc}", err=True)

    if failed:
        raise typer.Exit(code=1)


@app.command()
def preview(path: Path) -> None:
    settings = get_settings()
    repository = ContentRepository(settings.content_dir)
    brief = repository.load_brief(path)
    typer.echo(build_prompt(brief))


@app.command()
def generate(path: Path) -> None:
    settings = get_settings()
    repository = ContentRepository(settings.content_dir)
    generator = GeminiGenerator(settings)
    service = ContentGenerationService(
        repository=repository,
        generator=generator,
        output_dir=settings.output_dir,
        model_name=settings.gemini_model,
    )
    result = service.generate_from_file(path)
    typer.echo(result.text)
