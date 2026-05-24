"""Smoke tests for the scanmenow CLI entry point."""

from typer.testing import CliRunner
from scanmenow import __version__
from scanmenow.cli import app

runner = CliRunner()


def test_help_exits_zero():
    """uv run scanmenow --help exits 0 and contains usage text."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output


def test_help_mentions_app_name():
    """Help output includes the app name."""
    result = runner.invoke(app, ["--help"])
    assert "scanmenow" in result.output.lower()


def test_version_flag():
    """--version prints version and exits 0."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.output
