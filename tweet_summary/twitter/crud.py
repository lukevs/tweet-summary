import os
from datetime import datetime
from typing import Iterator, List, Optional

import requests
from ratelimit import limits, sleep_and_retry

from .schemas import Tweet, TweetPage


MAX_QUERY_SIZE = 512
API_BASE_URL = "https://api.twitter.com"
RECENT_SEARCH_ENDPOINT_URL = f"{API_BASE_URL}/2/tweets/search/recent"


def fetch_recent_tweets(
    auth_token: str, screen_names: List[str], since: datetime,
) -> Iterator[Tweet]:
    for query in _generate_from_or_queries(screen_names):
        next_token = None

        while True:
            tweet_page = _fetch_recent_tweets_page(
                auth_token, query, since, next_token,
            )

            yield from tweet_page.data

            next_token = tweet_page.meta.next_token
            if next_token is None:
                break


@sleep_and_retry
@limits(calls=1, period=2)
def _fetch_recent_tweets_page(
    auth_token: str,
    query: str,
    start_time: datetime,
    next_token: Optional[str] = None,
) -> TweetPage:
    tweet_fields = ",".join([
        "public_metrics",
        "referenced_tweets",
        "entities",
    ])

    params = {
        "query": query,
        "start_time": f"{start_time.isoformat()}",
        "tweet.fields": tweet_fields,
        "max_results": 100,
    }

    headers = {
        "Authorization": f"Bearer {auth_token}",
    }

    if next_token is not None:
        params["next_token"] = next_token

    response = requests.get(
        RECENT_SEARCH_ENDPOINT_URL,
        headers=headers,
        params=params,
    )

    if response.ok:
        return TweetPage(**response.json())
    else:
        raise RuntimeError(f"Failed to fetch tweet page: {response.text}")


def _generate_from_or_queries(screen_names: List[str]) -> Iterator[str]:
    if len(screen_names) == 0:
        return

    [first_screen_name, *rest_screen_names] = screen_names

    query = f"from:{first_screen_name}"

    for screen_name in rest_screen_names:
        from_screen_name = f"from:{screen_name}"
        query_update = f"{query} OR {from_screen_name}"

        if len(query_update) > MAX_QUERY_SIZE:
            yield query
            query = from_screen_name
        else:
            query = query_update

    yield query
