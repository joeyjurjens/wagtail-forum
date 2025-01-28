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
        related_name="reactions",  # Required related_name
    )


class Reply(AbstractReply):
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="replies",  # Required related_name
    )


class ReplyReaction(AbstractReplyReaction):
    reply = models.ForeignKey(
        Reply,
        on_delete=models.CASCADE,
        related_name="reactions",  # Required related_name
    )
