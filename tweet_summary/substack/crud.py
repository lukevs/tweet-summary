import os
import requests

from .schemas import (
    SubstackDraft,
    SubstackDraftBody,
    SubstackDraftBodyContent,
    SubstackDraftByline,
    SubstackDraftUpdate,
)


BASE_URL = "https://mltweets.substack.com"
DRAFTS_ENDPOINT = "/api/v1/drafts"

DEFAULT_DRAFT_BODY = SubstackDraftBody(
    type="doc",
    content=[SubstackDraftBodyContent(
        type="paragraph",
    )],
)

DEFAULT_DRAFT_BYLINE = SubstackDraftByline(
    id=21862228,
    name="Luke Van Seters",
    email="lukevanseters@gmail.com",
    photo_url="https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/0fd0f034-3ce9-45ab-9eb5-994b14b80e27_3447x4000.jpeg",
    bio=None,
    subscription_expiry="2120-12-06T21:31:30.764Z",
    subscription_type=None,
    subscription_id=33823131,
    stripe_subscription_id=None,
    stripe_platform_customer_id=None,
    anonymous_id=None,
    publisher_agreement_accepted_at="2020-12-05T21:27:09.014Z",
    is_contributor=True,
    is_admin=True,
    is_public_admin=True,
    has_saved_payment=False,
    is_free_subscribed=True,
    is_subscribed=True,
    email_disabled=False,
    podcast_email_disabled=False,
    has_pw=False,
    is_author=True,
)


def get_substack_cookie():
    return os.getenv("SUBSTACK_COOKIE")


def create_draft(title: str) -> SubstackDraft:
    draft = SubstackDraftUpdate(
        draft_title=title,
        draft_subtitle="",
        draft_bylines=[DEFAULT_DRAFT_BYLINE],
        draft_podcast_url="",
        draft_podcast_duration=None,
        draft_body=DEFAULT_DRAFT_BODY.json(),
        audience="everyone",
        type="newsletter",
    )

    url = BASE_URL + DRAFTS_ENDPOINT
    headers = {"Cookie": get_substack_cookie()}
    response = requests.post(url=url, headers=headers, json=draft.dict())
    return SubstackDraft(**response.json())
