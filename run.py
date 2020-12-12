import logging
from datetime import datetime, timedelta, timezone
from typing import List, Optional

import typer

from tweet_summary.twitter import fetch_recent_tweets
from tweet_summary.summarize import generate_tweet_summary


logging.basicConfig(
    filename='debug.log',
    format='%(asctime)s | %(levelname)s: %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.DEBUG,
)

app = typer.Typer()


def last_week() -> str:
    return (datetime.now(timezone.utc) - timedelta(days=7) + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")


def yesterday() -> str:
    return (datetime.now(timezone.utc) - timedelta(days=1) + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")


@app.command()
def fetch(
    screen_names: typer.FileText,
    since: datetime = typer.Argument(yesterday),
):
    tweets = fetch_recent_tweets(
        screen_names.read().split(), since,
    )

    for tweet in tweets:
        typer.echo(tweet.json())


@app.command()
def summarize(
    screen_names: typer.FileText,
    since: datetime = typer.Argument(yesterday),
):
    tweets = fetch_recent_tweets(
        screen_names.read().split(), since,
    )

    summary = generate_tweet_summary(tweets)

    typer.echo(summary.json())


if __name__ == "__main__":
    app()
