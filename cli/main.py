"""
Command-line interface for the IntelliDoc project.

This CLI uses the `typer` library to provide a user-friendly interface for processing
documents and interacting with the IntelliDoc API.  Additional commands can be added
as the project evolves.
"""

import typer

app = typer.Typer(help="IntelliDoc command-line interface")


@app.command()
def process(file: str) -> None:
    """Process a single file using the IntelliDoc API.

    Args:
        file: Path to the document to process.
    """
    typer.echo(f"Processing document: {file}")
    # TODO: Implement API call to IntelliDoc backend


@app.command()
def version() -> None:
    """Print the version of the IntelliDoc CLI."""
    typer.echo("IntelliDoc CLI version 0.1.0")


if __name__ == "__main__":
    app()
