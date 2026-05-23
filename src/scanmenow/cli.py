"""ScanMeNow CLI entry point."""

import typer
from typing import Optional
from scanmenow import __version__

app = typer.Typer(
    name="scanmenow",
    help="Data governance platform for discovering and managing sensitive data.",
    no_args_is_help=True,
)


def version_callback(value: bool) -> None:
    if value:
        typer.echo(f"scanmenow {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
) -> None:
    """ScanMeNow — data governance platform."""


if __name__ == "__main__":
    app()
