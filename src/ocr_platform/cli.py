from pathlib import Path

import typer

from .service import recognize_file

app = typer.Typer(
    help="Run OCR digit recognition from the command line.",
    no_args_is_help=True,
)


@app.command("predict")
def predict(image_path: Path) -> None:
    """Predict handwritten digits from an image path."""
    result = recognize_file(image_path)
    typer.echo(result.model_dump_json(indent=2))


@app.command("version")
def version() -> None:
    """Show CLI version."""
    typer.echo("ocr-digit-recognition-platform 1.0.0")


if __name__ == "__main__":
    app()
