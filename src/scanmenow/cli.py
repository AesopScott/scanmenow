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
    """ScanMeNow -- data governance platform."""


@app.command()
def retain(
    max_age_days: int = typer.Option(
        ...,
        "--max-age-days",
        help="Delete findings older than this many days.",
        min=1,
    ),
    dry_run: bool = typer.Option(
        True,
        "--dry-run/--confirm",
        help=(
            "Dry-run mode (default): report candidates but perform no deletions. "
            "Pass --confirm to perform live deletions."
        ),
    ),
    backend: Optional[str] = typer.Option(
        None,
        "--backend",
        help=(
            "Storage backend override ('sqlite' or 'firestore'). "
            "Defaults to SCANMENOW_BACKEND env var or 'sqlite'."
        ),
    ),
) -> None:
    """Evaluate and optionally enforce the data retention policy.

    In dry-run mode (default), scans for findings older than MAX_AGE_DAYS days
    and reports how many would be deleted without touching the database.

    Pass --confirm to perform live deletions.

    Examples
    --------
    # Report what would be deleted (safe, no changes):
    scanmenow retain --max-age-days 90

    # Actually delete findings older than 90 days:
    scanmenow retain --max-age-days 90 --confirm
    """
    from scanmenow.storage.base import get_repository
    from scanmenow.retention.policy import RetentionPolicy
    from scanmenow.retention.evaluator import evaluate_retention

    repo = get_repository(backend=backend)
    policy = RetentionPolicy(max_age_days=max_age_days, dry_run=dry_run)

    mode_label = "DRY RUN" if dry_run else "LIVE"
    typer.echo(
        f"[{mode_label}] Evaluating retention policy: "
        f"findings older than {max_age_days} day(s)."
    )

    report = evaluate_retention(repo, policy)

    typer.echo(f"  Candidates found : {report.candidate_count}")

    if dry_run:
        typer.echo(
            "  No deletions performed (dry-run). "
            "Re-run with --confirm to delete."
        )
    else:
        typer.echo(f"  Deleted          : {report.deleted_count}")

    if report.candidate_count == 0:
        typer.echo("  Nothing to do.")


if __name__ == "__main__":
    app()
