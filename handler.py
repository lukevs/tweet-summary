import os
import logging

from datetime import datetime, timedelta, timezone
from typing import List, Optional

from tweet_summary.twitter import fetch_recent_tweets
from tweet_summary.summarize import generate_tweet_summary


logger = logging.getLogger()
logger.setLevel(logging.INFO)


SCREEN_NAMES_FILEPATH = "data/screen_names.txt"


def last_week() -> datetime:
    return (datetime.now(timezone.utc) - timedelta(days=7) + timedelta(hours=1))


def yesterday() -> datetime:
    return (datetime.now(timezone.utc) - timedelta(days=1) + timedelta(hours=1))


def handler(event, context) -> str:
    logger.info("Starting")
    logger.info(f"EVENT: {event}")

    with open(SCREEN_NAMES_FILEPATH, "r") as names_file:
        screen_names = names_file.read().split()

    auth_token = os.getenv("TWITTER_TOKEN")

    since = yesterday()
    tweets = fetch_recent_tweets(auth_token, screen_names, since)
    summary = generate_tweet_summary(tweets)

    return summary.json()
