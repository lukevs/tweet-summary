from typing import List

from pydantic import BaseModel

from tweet_summary.twitter import Tweet


class MentionSummary(BaseModel):
    screen_name: str
    total_references: int


class LinkSummary(BaseModel):
    url: str
    total_references: int


class ReferencedTweetSummary(BaseModel):
    tweet_id: str
    total_references: int


class TweetSummary(BaseModel):
    total_tweets: int
    most_liked_tweets: List[Tweet]
    most_retweeted_tweets: List[Tweet]
    most_referenced_tweets: List[ReferencedTweetSummary]
    most_referenced_links: List[LinkSummary]
    most_mentioned_screen_names: List[MentionSummary]
    most_referenced_arxiv_links: List[LinkSummary]
