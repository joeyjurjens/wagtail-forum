from django.conf import settings
from django.utils.translation import pgettext_lazy

TOPIC_REACTION_TYPES = getattr(
    settings,
    "WAGTAIL_FORUM_TOPIC_REACTION_TYPES",
    [
        ("like", pgettext_lazy("wagtail_forum", "Like")),
        ("dislike", pgettext_lazy("wagtail_forum", "Dislike")),
    ],
)
REPLY_REACTION_TYPES = getattr(
    settings,
    "WAGTAIL_FORUM_REPLY_REACTION_TYPES",
    [
        ("like", pgettext_lazy("wagtail_forum", "Like")),
        ("dislike", pgettext_lazy("wagtail_forum", "Dislike")),
    ],
)
