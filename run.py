from datetime import datetime, timedelta
from typing import Optional

import typer


app = typer.Typer()


@app.command()
def summarize(usernames: typer.FileText, since: datetime = typer.Argument(yesterday)):
    typer.echo(usernames.read())


def yesterday() -> str:
    return (datetime.now() - timedelta(1)).strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    app()