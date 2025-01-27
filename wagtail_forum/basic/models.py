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
    pass


class Forum(AbstractForum):
    pass
    # parent_page_types = ["wagtail_forum_basic.Index", "wagtail_forum_basic.Forum"]
    # subpage_types = ["wagtail_forum_basic.Forum", "wagtail_forum_basic.Topic"]


class Topic(AbstractTopic):
    pass


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
