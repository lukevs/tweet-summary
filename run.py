from datetime import datetime, timedelta, timezone
from typing import List, Optional

import typer

from tweet_summary.twitter import fetch_recent_tweets
from tweet_summary.summarize import generate_tweet_summary


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
    tweets = fetch_recent_tweets(
        screen_names.read().split(), since,
    )

    summary = generate_tweet_summary(tweets)

    typer.echo(f"Summary: {summary}")


if __name__ == "__main__":
    app()
