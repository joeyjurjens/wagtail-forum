from django.db import models

from wagtail_forum.abstract_models import (
    AbstractForumIndex,
    AbstractForum,
    AbstractTopic,
    AbstractTopicReaction,
    AbstractReply,
    AbstractReplyReaction,
)


class Index(AbstractForumIndex):
    subpage_types = ["Forum"]


class Forum(AbstractForum):
    parent_page_types = ["Index"]
    subpage_types = ["Topic", "Forum"]


class Topic(AbstractTopic):
    parent_page_types = ["Forum"]
    subpage_types = []


class TopicReaction(AbstractTopicReaction):
    topic = models.ForeignKey(
        "Topic", on_delete=models.CASCADE, related_name="reactions"
    )


class Reply(AbstractReply):
    topic = models.ForeignKey("Topic", on_delete=models.CASCADE, related_name="replies")


class ReplyReaction(AbstractReplyReaction):
    reply = models.ForeignKey(
        "Reply", on_delete=models.CASCADE, related_name="reactions"
    )
