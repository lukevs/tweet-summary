from typing import List, Optional

from pydantic import BaseModel


class TweetMention(BaseModel):
    username: str


class TweetEntityUrl(BaseModel):
    expanded_url: str
    unwound_url: Optional[str]


class TweetEntities(BaseModel):
    urls: List[TweetEntityUrl] = []
    mentions: List[TweetMention] = []


class ReferencedTweet(BaseModel):
    id: str


class TweetPublicMetrics(BaseModel):
    like_count: int
    retweet_count: int


class Tweet(BaseModel):
    id: str
    public_metrics: TweetPublicMetrics
    referenced_tweets: List[ReferencedTweet] = []
    entities: Optional[TweetEntities]


class TweetPageMeta(BaseModel):
    next_token: Optional[str]


class TweetPage(BaseModel):
    data: List[Tweet] = []
    meta: TweetPageMeta


class TwitterUser(BaseModel):
    id: str
