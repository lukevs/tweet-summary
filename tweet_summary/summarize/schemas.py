from typing import List

from pydantic import BaseModel

from tweet_summary.twitter import Tweet


class ReferencedTweetSummary(BaseModel):
    tweet_id: str
    total_references: int


class TweetSummary(BaseModel):
    most_liked_tweets: List[Tweet]
    most_retweeted_tweets: List[Tweet]
    most_referenced_tweets: List[ReferencedTweetSummary]
