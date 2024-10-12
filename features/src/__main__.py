"""Main."""

from pathlib import Path
from typing import Any

import click
from oml.register.repo_operations import apply_total, plan
from oml.register.store import repo_config

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


@click.group(context_settings=CONTEXT_SETTINGS)
def cli() -> Any:
    """The Register CLI to manage the ml-team feature store.

    Commands:
        plan        Plan Features
        apply       Apply Features
    """


@click.group(hidden=True)
def features() -> None:
    """Features commands."""


@features.command(hidden=True, name="plan")
def plan_cmd() -> None:
    """Plan features."""
    from oml.register import feature_views

    plan(repo_config, Path(f"{feature_views.__path__[0]}"), True)


@features.command(hidden=True, name="apply")
def apply_cmd() -> None:
    """Apply features."""
    from oml.register import feature_views

    apply_total(repo_config, Path(f"{feature_views.__path__[0]}"), True)


cli.add_command(features)

if __name__ == "__main__":
    cli()
