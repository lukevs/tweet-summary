from typing import List

from pydantic import BaseModel

from tweet_summary.twitter import Tweet


class TweetSummary(BaseModel):
    most_liked_tweets: List[Tweet]
    most_retweeted_tweets: List[Tweet]
