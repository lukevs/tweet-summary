from collections import Counter
from itertools import islice, tee
from typing import Callable, Iterator, List

from tweet_summary.twitter import Tweet

from .schemas import (
    LinkSummary, MentionSummary, ReferencedTweetSummary, TweetSummary,
)


def generate_tweet_summary(
    tweets: Iterator[Tweet], top_n: int = 10,
) -> TweetSummary:
    (
        like_tweets,
        retweet_tweets,
        reference_tweets,
        link_tweets,
        mention_tweets,
        count_tweets,
    ) = tee(tweets, 6)

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

    most_referenced_links = get_most_referenced_links(
        link_tweets, top_n,
    )

    most_mentioned_screen_names = get_most_mentioned_screen_names(
        mention_tweets, top_n,
    )

    total_tweets = get_total_tweets(count_tweets)

    return TweetSummary(
        total_tweets=total_tweets,
        most_liked_tweets=most_liked_tweets,
        most_retweeted_tweets=most_retweeted_tweets,
        most_referenced_tweets=most_referenced_tweets,
        most_referenced_links=most_referenced_links,
        most_mentioned_screen_names=most_mentioned_screen_names,
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
) -> List[ReferencedTweetSummary]:
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


def get_most_referenced_links(
    tweets: Iterator[Tweet], top_n: int,
) -> List[LinkSummary]:
    counter = Counter(
        url.unwound_url or url.expanded_url
        for tweet in tweets
        if tweet.entities is not None
        for url in tweet.entities.urls
    )

    return [
        LinkSummary(url=url, total_references=count)
        for url, count in counter.most_common(top_n)
    ]


def get_most_mentioned_screen_names(
    tweets: Iterator[Tweet], top_n: int,
) -> List[MentionSummary]:
    counter = Counter(
        mention.username
        for tweet in tweets
        if tweet.entities is not None
        for mention in tweet.entities.mentions
    )

    return [
        MentionSummary(screen_name=screen_name, total_references=count)
        for screen_name, count in counter.most_common(top_n)
    ]


def get_total_tweets(tweets: Iterator[Tweet]) -> int:
    return sum(1 for _ in tweets)
