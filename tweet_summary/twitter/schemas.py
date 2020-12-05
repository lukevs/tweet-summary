from typing import List, Optional

from pydantic import BaseModel


class TweetPublicMetrics(BaseModel):
    like_count: int


class Tweet(BaseModel):
    id: str
    public_metrics: TweetPublicMetrics


class TweetPageMeta(BaseModel):
    next_token: Optional[str]


class TweetPage(BaseModel):
    data: List[Tweet] = []
    meta: TweetPageMeta
