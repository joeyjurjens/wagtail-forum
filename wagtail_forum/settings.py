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

DEFAULT_QUILL_EDITOR_CONFIG = {
    "modules": {
        "toolbar": [
            [
                {"header": "2"},
                {"header": "3"},
                {"header": "4"},
                {"header": "5"},
                {"header": "6"},
            ],
            [
                "bold",
                "italic",
                "underline",
                "strike",
                "clean",
            ],
            [
                {"color": []},
                {"background": []},
            ],
            [
                "link",
                # "image",
                "code",
            ],
            [
                {"list": "ordered"},
                {"list": "bullet"},
            ],
        ],
    },
    "theme": "snow",
    "placeholder": "",
}

QUILL_EDITOR_CONFIG = getattr(
    settings, "WAGTAIL_FORUM_QUILL_EDITOR_CONFIG", DEFAULT_QUILL_EDITOR_CONFIG
)
