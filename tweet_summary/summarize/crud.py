import itertools
from typing import Iterator

from tweet_summary.twitter import Tweet

from .schemas import TweetSummary


def generate_tweet_summary(tweets: Iterator[Tweet], top_n: int = 10) -> TweetSummary:
    tweets_sorted_by_likes = sorted(
        tweets, key=lambda tweet: -tweet.public_metrics.like_count,
    )

    most_liked_tweets = list(
        itertools.islice(tweets_sorted_by_likes, top_n)
    )

    return TweetSummary(
        most_liked_tweets=most_liked_tweets,
    )
