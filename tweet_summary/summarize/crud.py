from collections import Counter
from itertools import islice, tee
from typing import Callable, Iterator, List
from urllib.parse import urlparse

from tweet_summary.twitter import Tweet
from tweet_summary.substack import SubstackDraftDoc

from .schemas import (
    LinkSummary, MentionSummary, ReferencedTweetSummary, TweetSummary,
)


# def format_substack_draft(summary: TweetSummary) -> SubstackDraftDoc:
#     total_tweets = SubstackDraftParagraph(
#         content=[SubstackDraftText(
#             text=f"Total tweets: {summary.total_tweets}",
#         )],
#     )
# 
#     most_liked_tweets_heading = SubstackDraftHeading(
#         attrs=SubstackDraftAttrs(level=3),
#         content=[SubstackDraftText(text="MOST_LIKED_TWEETS")],
#     )
# 
#     most_liked_tweets = [
#         SubstackDraftParagraph(
#             content=[SubstackDraftText(text=tweet.id)],
#         )
#         for tweet in summary.most_liked_tweets
#     ]
# 
#     return SubstackDraftDoc(
#         content=[
#             total_tweets,
#             most_liked_tweets_heading,
#             **most_liked_tweets,
#         ],
#     )


def generate_tweet_summary(
    tweets: Iterator[Tweet], top_n: int = 10,
) -> TweetSummary:
    summarizers = {
        "total_tweets": get_total_tweets,
        "most_liked_tweets": get_most_liked_tweets,
        "most_retweeted_tweets": get_most_retweeted_tweets,
        "most_referenced_tweets": get_most_referenced_tweet_ids,
        "most_referenced_links": get_most_referenced_links,
        "most_mentioned_screen_names": get_most_mentioned_screen_names,
        "most_referenced_arxiv_links": get_most_referenced_arxiv_links,
    }

    tweet_iterators = tee(tweets, len(summarizers))

    summaries = {}

    for (key, summarize), tweets in zip(summarizers.items(), tweet_iterators):
        summaries[key] = summarize(tweets)

    return TweetSummary(**summaries)


def get_most_liked_tweets(tweets: Iterator[Tweet]) -> List[Tweet]:
    return get_top_n_tweets(
        tweets,
        top_n=10,
        key=lambda tweet: tweet.public_metrics.like_count,
    )


def get_most_retweeted_tweets(tweets: Iterator[Tweet]) -> List[Tweet]:
    return get_top_n_tweets(
        tweets,
        top_n=10,
        key=lambda tweet: tweet.public_metrics.retweet_count,
    )


def get_top_n_tweets(
    tweets: Iterator[Tweet], top_n: int, key: Callable[[Tweet], int],
) -> List[Tweet]:
    tweets_sorted = sorted(
        tweets, key=lambda tweet: -key(tweet),
    )

    return list(islice(tweets_sorted, top_n))


def get_most_referenced_tweet_ids(
    tweets: Iterator[Tweet], top_n: int = 10,
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
    tweets: Iterator[Tweet], top_n: int = 10, link_filter = None,
) -> List[LinkSummary]:
    urls = (
        url.unwound_url or url.expanded_url
        for tweet in tweets
        if tweet.entities is not None
        for url in tweet.entities.urls
    )


    filtered_urls = (
        url for url in urls
        if not link_filter or link_filter(url)
    )

    counter = Counter(filtered_urls)

    return [
        LinkSummary(url=url, total_references=count)
        for url, count in counter.most_common(top_n)
    ]


def get_most_referenced_arxiv_links(tweets: Iterator[Tweet]) -> List[LinkSummary]:
    return get_most_referenced_links(tweets, link_filter=is_arxiv)


def is_arxiv(url: str) -> bool:
    domain = urlparse(url).netloc.lower()
    arxiv_domain = "arxiv.org"
    return domain == arxiv_domain or domain.endswith(f".{arxiv_domain}")


def get_most_mentioned_screen_names(
    tweets: Iterator[Tweet], top_n: int = 10,
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
