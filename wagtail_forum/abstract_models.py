from django.db import models
from django.conf import settings
from django.utils.translation import pgettext_lazy

from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.fields import RichTextField
from wagtail.models import Page

from . import settings as forum_settings
from .mixins import RequiredForeignKeyMixin


class AbstractForumIndex(RoutablePageMixin, Page):
    class Meta:
        abstract = True
        verbose_name = pgettext_lazy("wagtail_forum", "Forum index")
        verbose_name_plural = pgettext_lazy("wagtail_forum", "Forum index")

    wagtail_forum_template = "wagtail_forum/pages/forum_index.html"

    def get_template(self, request, *args, **kwargs):
        return self.wagtail_forum_template

    def get_context(self, request, *args, **kwargs):
        ctx = super().get_context(request, *args, **kwargs)
        ctx["root_forums"] = self.get_root_forums()
        return ctx

    def get_root_forums(self):
        return [
            forum_page.specific
            for forum_page in self.get_children().type(AbstractForum).live()
        ]


class AbstractForum(RoutablePageMixin, Page):
    class Meta:
        abstract = True
        verbose_name = pgettext_lazy("wagtail_forum", "Forum")
        verbose_name_plural = pgettext_lazy("wagtail_forum", "Forums")

    wagtail_forum_template = "wagtail_forum/pages/forum.html"

    def get_template(self, request, *args, **kwargs):
        return self.wagtail_forum_template

    @route(r"^create-topic/$", name="create_topic")
    def create_topic(self, request):
        pass

    def get_context(self, request, *args, **kwargs):
        ctx = super().get_context(request, *args, **kwargs)
        ctx["sub_forums"] = self.get_sub_forums()
        return ctx

    def get_sub_forums(self):
        return [
            sub_forum.specific
            for sub_forum in self.get_children().type(AbstractForum).live()
        ]

    @property
    def has_sub_forums(self):
        return any(self.get_sub_forums())


class AbstractTopic(RoutablePageMixin, Page):
    class Meta:
        abstract = True
        verbose_name = pgettext_lazy("wagtail_forum", "Topic")
        verbose_name_plural = pgettext_lazy("wagtail_forum", "Topics")

    content = RichTextField(
        blank=True,
        help_text=pgettext_lazy("wagtail_forum", "The content of the topic."),
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="forum_topics",
        help_text=pgettext_lazy("wagtail_forum", "The user who created the topic."),
    )

    wagtail_forum_template = "wagtail_forum/pages/topic.html"

    def get_template(self, request, *args, **kwargs):
        return self.wagtail_forum_template

    @route(r"^edit/$", name="edit")
    def edit(self, request):
        pass

    @route(r"^reply/$", name="reply")
    def reply(self, request):
        pass

    @route(r"^react/$", name="react")
    def react(self, request):
        pass


class AbstractTopicReaction(RequiredForeignKeyMixin, models.Model):
    class Meta:
        abstract = True
        unique_together = ("user", "topic")
        verbose_name = pgettext_lazy("wagtail_forum", "Topic reaction")
        verbose_name_plural = pgettext_lazy("wagtail_forum", "Topic reactions")

    REQUIRED_FOREIGN_KEYS = [("topic", "reactions")]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="forum_topic_reactions",
        help_text=pgettext_lazy("wagtail_forum", "The user who reacted to the topic."),
    )
    reaction_type = models.CharField(
        max_length=255,
        choices=forum_settings.TOPIC_REACTION_TYPES,
        help_text=pgettext_lazy("wagtail_forum", "The type of reaction."),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=pgettext_lazy(
            "wagtail_forum", "The date and time the reaction was created."
        ),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=pgettext_lazy(
            "wagtail_forum", "The date and time the reaction was last updated."
        ),
    )


class AbstractReply(RequiredForeignKeyMixin, models.Model):
    class Meta:
        abstract = True
        verbose_name = pgettext_lazy("wagtail_forum", "Reply")
        verbose_name_plural = pgettext_lazy("wagtail_forum", "Replies")

    REQUIRED_FOREIGN_KEYS = [("topic", "replies")]

    content = RichTextField(
        help_text=pgettext_lazy("wagtail_forum", "The content of the reply."),
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="forum_topic_replies",
        help_text=pgettext_lazy("wagtail_forum", "The user who created the reply."),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=pgettext_lazy(
            "wagtail_forum", "The date and time the reply was created."
        ),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=pgettext_lazy(
            "wagtail_forum", "The date and time the reply was last updated."
        ),
    )


class AbstractReplyReaction(RequiredForeignKeyMixin, models.Model):
    class Meta:
        abstract = True
        unique_together = ("user", "reply")
        verbose_name = pgettext_lazy("wagtail_forum", "Reply reaction")
        verbose_name_plural = pgettext_lazy("wagtail_forum", "Reply reactions")

    REQUIRED_FOREIGN_KEYS = [("reply", "reactions")]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="forum_reply_reactions",
        help_text=pgettext_lazy("wagtail_forum", "The user who reacted to the reply."),
    )
    reaction_type = models.CharField(
        max_length=255,
        choices=forum_settings.REPLY_REACTION_TYPES,
        help_text=pgettext_lazy("wagtail_forum", "The type of reaction."),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=pgettext_lazy(
            "wagtail_forum", "The date and time the reaction was created."
        ),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=pgettext_lazy(
            "wagtail_forum", "The date and time the reaction was last updated."
        ),
    )
