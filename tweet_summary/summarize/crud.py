from itertools import islice, tee
from typing import Callable, Iterator, List

from tweet_summary.twitter import Tweet

from .schemas import TweetSummary


def generate_tweet_summary(
    tweets: Iterator[Tweet], top_n: int = 10,
) -> TweetSummary:
    like_tweets, retweet_tweets = tee(tweets, 2)

    most_liked_tweets = get_top_n_tweets(
        like_tweets,
        top_n,
        key=lambda tweet: tweet.public_metrics.like_count,
    )

    most_retweeted_tweets = get_top_n_tweets(
        retweet_tweets,
        top_n,
        key=lambda tweet: tweet.public_metrics.retweet_count,
    )

    return TweetSummary(
        most_liked_tweets=most_liked_tweets,
        most_retweeted_tweets=most_retweeted_tweets,
    )


def get_top_n_tweets(
    tweets: Iterator[Tweet], top_n: int, key: Callable[[Tweet], int],
) -> List[Tweet]:
    tweets_sorted = sorted(
        tweets, key=lambda tweet: -key(tweet),
    )

    return list(islice(tweets_sorted, top_n))
