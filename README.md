# wagtail-forum

A flexible forum application for Wagtail CMS that allows you to add one or multiple forums to your website.
Built with customization in mind, it provides abstract models that you can extend to create your own forum implementation.

## Quick Start

1. Install the package:

```bash
pip install wagtail-forum
```

2. Add "wagtail_forum" to your INSTALLED_APPS setting:

```python
INSTALLED_APPS = [
    ...
    "wagtail_forum",
    # Optional basic API package
    "wagtail_forum.contrib.api",
]
```

## Setup

This package provides no default implementation for the forum models.
You need to create your own models that extend the abstract models provided by this package.

In the future, I might built a more opinionated implementation as a separate package or contrib app.

A minimal setup looks like this:

```python
from django.db import models

from wagtail_forum.abstract_models import (
    AbstractForumIndex,
    AbstractForum,
    AbstractTopic,
    AbstractTopicReaction,
    AbstractReply,
    AbstractReplyReaction,
)

class ForumIndex(AbstractForumIndex):
    pass

class Forum(AbstractForum):
    pass

class Topic(AbstractTopic):
    pass

class TopicReaction(AbstractTopicReaction):
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="reactions"  # Required related_name
    )

class Reply(AbstractReply):
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="replies"  # Required related_name
    )

class ReplyReaction(AbstractReplyReaction):
    reply = models.ForeignKey(
        Reply,
        on_delete=models.CASCADE,
        related_name="reactions"  # Required related_name
    )
```

With this setup, you can add the fields you need for your forum while keeping the functionality provided by the abstract models.

### Customizing RouteablePageMixin routes logic

The abstract models inherit from `RouteablePageMixin` to allow adding sub routes to the forum pages.
Some of the abstract models have predefined routes;

AbstractForum:
```python
class AbstractForum(RoutablePageMixin, Page):
    ...
    create_topic_view_class = TopicCreateView

    @route(r"^create-topic/$", name="create_topic")
    def create_topic(self, request):
        # Try to find a subpage model that is a subclass of AbstractTopic
        model = next(
            (
                model
                for model in self.allowed_subpage_models()
                if issubclass(model, AbstractTopic)
            ),
            None,
        )
        return self.create_topic_view_class.as_view(
            model=model, template_name="wagtail_forum/pages/forum_topic_create.html"
        )(request)
```

AbstractTopic:

```python
class AbstractTopic(RoutablePageMixin, Page):
    ...
    edit_view_class = TopicEditView
    reply_view_class = TopicReplyView
    react_view_class = TopicReactView

    @route(r"^edit/$", name="edit")
    def edit(self, request):
        return self.edit_view_class.as_view(instance=self)(request)

    @route(r"^reply/$", name="reply")
    def reply(self, request):
        return self.reply_view_class.as_view(instance=self)(request)

    @route(r"^react/$", name="react")
    def react(self, request):
        return self.react_view_class.as_view(instance=self)(request)
```

The reason that the routes return class based views is to prevent cluttering the models with view logic while still allowing for easy customization.

You can override the view classes by setting the class attributes on your custom models, eg;

```python
class CustomTopic(AbstractTopic):
    edit_view_class = CustomTopicEditView
```

Because it inherits from `RouteablePageMixin`, you can add your own routes to the models as well.
If you want to disable some, just override the route method and return None.

```python
class CustomTopic(AbstractTopic):
    ...
    @route(r"^edit/$", name="edit")
    def edit(self, request):
        return None
```

## Settings

Available settings in your Django settings:

```python
# Reaction types for topics
WAGTAIL_FORUM_TOPIC_REACTION_TYPES = [
    ('like', '👍'),
    ('dislike', '👎'),
    # Add your custom reactions
]

# Reaction types for replies
WAGTAIL_FORUM_REPLY_REACTION_TYPES = [
    ('like', '👍'),
    ('dislike', '👎'),
    # Add your custom reactions
]

# Quill editor configuration, please see https://quilljs.com/docs/configuration/ for options
# This setting is json dumped and passed to the Quill editor
WAGTAIL_FORUM_QUILL_EDITOR_CONFIG = {
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
```

## Templates & Customization

The forum pages and views inherit from "wagtail_forum/base.html".

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
