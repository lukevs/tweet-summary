from collections import Counter
from itertools import islice, tee
from typing import Callable, Iterator, List

from tweet_summary.twitter import Tweet

from .schemas import ReferencedTweetSummary, TweetSummary


def generate_tweet_summary(
    tweets: Iterator[Tweet], top_n: int = 10,
) -> TweetSummary:
    (
            like_tweets, retweet_tweets, reference_tweets,
    ) = tee(tweets, 3)

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

    most_referenced_tweets = get_most_referenced_tweet_ids(
        reference_tweets, top_n,
    )

    return TweetSummary(
        most_liked_tweets=most_liked_tweets,
        most_retweeted_tweets=most_retweeted_tweets,
        most_referenced_tweets=most_referenced_tweets,
    )


def get_top_n_tweets(
    tweets: Iterator[Tweet], top_n: int, key: Callable[[Tweet], int],
) -> List[Tweet]:
    tweets_sorted = sorted(
        tweets, key=lambda tweet: -key(tweet),
    )

    return list(islice(tweets_sorted, top_n))


def get_most_referenced_tweet_ids(
    tweets: Iterator[Tweet], top_n: int,
) -> List[str]:
    counter = Counter(
        referenced_tweet.id
        for tweet in tweets
        for referenced_tweet in tweet.referenced_tweets
    )

    return [
        ReferencedTweetSummary(
            tweet_id=tweet_id,
            total_references=count,
        )
        for tweet_id, count in counter.most_common(top_n)
    ]
