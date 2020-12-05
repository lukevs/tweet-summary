from typing import List, Optional

from pydantic import BaseModel


class ReferencedTweet(BaseModel):
    id: str


class TweetPublicMetrics(BaseModel):
    like_count: int
    retweet_count: int


class Tweet(BaseModel):
    id: str
    public_metrics: TweetPublicMetrics
    referenced_tweets: List[ReferencedTweet] = []


class TweetPageMeta(BaseModel):
    next_token: Optional[str]


class TweetPage(BaseModel):
    data: List[Tweet] = []
    meta: TweetPageMeta
