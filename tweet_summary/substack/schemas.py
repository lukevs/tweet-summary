from typing import List, Optional

from pydantic import BaseModel


class SubstackDraftByline(BaseModel):
    id: int
    name: str
    email: str
    photo_url: str
    bio: Optional[str]
    subscription_expiry: str
    subscription_type: Optional[str]
    subscription_id: int
    stripe_subscription_id: Optional[str]
    stripe_platform_customer_id: Optional[str]
    anonymous_id: Optional[str]
    publisher_agreement_accepted_at: str
    is_contributor: bool
    is_admin: bool
    is_public_admin: bool
    has_saved_payment: bool
    is_free_subscribed: bool
    is_subscribed: bool
    email_disabled: bool
    podcast_email_disabled: bool
    has_pw: bool
    is_author: bool


class SubstackDraftBodyContent(BaseModel):
    type: str


class SubstackDraftBody(BaseModel):
    type: str
    content: List[SubstackDraftBodyContent]


class SubstackDraftUpdate(BaseModel):
    draft_title: str
    draft_subtitle: str
    draft_bylines: List[SubstackDraftByline]
    draft_podcast_url: str
    draft_podcast_duration: Optional[str]
    draft_body: str
    audience: str
    type: str


class SubstackDraft(BaseModel):
    id: str
