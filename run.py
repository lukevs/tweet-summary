from datetime import datetime, timedelta, timezone
from typing import List, Optional

import typer

from twitter import fetch_most_liked_tweet, fetch_recent_tweets


app = typer.Typer()


def yesterday() -> str:
    return (datetime.now(timezone.utc) - timedelta(1)).strftime("%Y-%m-%d %H:%M:%S")


@app.command()
def fetch(
    screen_names: typer.FileText,
    since: datetime = typer.Argument(yesterday),
):
    tweets = fetch_recent_tweets(
        screen_names.read().split(), since,
    )

    for tweet in tweets:
        typer.echo(tweet)


@app.command()
def summarize(
    screen_names: typer.FileText,
    since: datetime = typer.Argument(yesterday),
):
    tweet = fetch_most_liked_tweet(
        screen_names.read().split(), since,
    )

    typer.echo(f"Most liked tweet since {since}: {tweet}")


if __name__ == "__main__":
    app()
