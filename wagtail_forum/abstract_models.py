from django.apps import apps
from django.db import models
from django.conf import settings
from django.utils.translation import pgettext_lazy

from wagtail.admin.panels import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.models import Page

from . import settings as forum_settings
from .fields import QuillRichTextField
from .mixins import RequiredForeignKeyMixin
from .views import (
    TopicCreateView,
    TopicEditView,
    TopicReplyView,
    TopicReactView,
)


class AbstractForumIndex(RoutablePageMixin, Page):
    class Meta:
        abstract = True
        verbose_name = pgettext_lazy("wagtail_forum", "Forum index")
        verbose_name_plural = pgettext_lazy("wagtail_forum", "Forum index")

    wagtail_forum_template = "wagtail_forum/pages/forum_index.html"

    def get_template(self, request, *args, **kwargs):
        return self.wagtail_forum_template

    @property
    def root_forums(self):
        return [
            forum_page.specific
            for forum_page in self.get_children().type(AbstractForum).live()
        ]

    @classmethod
    def allowed_subpage_models(cls):
        if not hasattr(cls, "subpage_types"):
            return [
                model
                for model in apps.get_app_config(cls._meta.app_label).get_models()
                if issubclass(model, AbstractForum) and not model._meta.abstract
            ]
        return super().allowed_subpage_models()


class AbstractForum(RoutablePageMixin, Page):
    class Meta:
        abstract = True
        verbose_name = pgettext_lazy("wagtail_forum", "Forum")
        verbose_name_plural = pgettext_lazy("wagtail_forum", "Forums")

    wagtail_forum_template = "wagtail_forum/pages/forum.html"

    create_topic_view_class = TopicCreateView

    def get_template(self, request, *args, **kwargs):
        return self.wagtail_forum_template

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
            model=model,
            forum=self,
            template_name="wagtail_forum/pages/create_topic.html",
        )(request)

    @property
    def sub_forums(self):
        return [
            sub_forum.specific
            for sub_forum in self.get_children().type(AbstractForum).live()
        ]

    @property
    def topics(self):
        return [
            topic.specific for topic in self.get_children().type(AbstractTopic).live()
        ]

    @classmethod
    def allowed_subpage_models(cls):
        if not hasattr(cls, "subpage_types"):
            return [
                model
                for model in apps.get_app_config(cls._meta.app_label).get_models()
                if issubclass(model, (AbstractForum, AbstractTopic))
                and not model._meta.abstract
            ]
        return super().allowed_subpage_models

    @classmethod
    def allowed_parent_page_models(cls):
        if not hasattr(cls, "parent_page_types"):
            return [
                model
                for model in apps.get_app_config(cls._meta.app_label).get_models()
                if issubclass(model, AbstractForumIndex) and not model._meta.abstract
            ]
        return super().allowed_parent_page_models()


class AbstractTopic(RoutablePageMixin, Page):
    class Meta:
        abstract = True
        verbose_name = pgettext_lazy("wagtail_forum", "Topic")
        verbose_name_plural = pgettext_lazy("wagtail_forum", "Topics")

    content = QuillRichTextField(
        help_text=pgettext_lazy("wagtail_forum", "The content of the topic."),
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="forum_topics",
        help_text=pgettext_lazy("wagtail_forum", "The user who created the topic."),
    )

    content_panels = Page.content_panels + [
        FieldPanel("content"),
    ]

    wagtail_forum_template = "wagtail_forum/pages/topic.html"

    edit_view_class = TopicEditView
    reply_view_class = TopicReplyView
    react_view_class = TopicReactView

    def get_template(self, request, *args, **kwargs):
        return self.wagtail_forum_template

    @route(r"^edit/$", name="edit")
    def edit(self, request):
        return self.edit_view_class.as_view(instance=self)(request)

    @route(r"^reply/$", name="reply")
    def reply(self, request):
        return self.reply_view_class.as_view(instance=self)(request)

    @route(r"^react/$", name="react")
    def react(self, request):
        return self.react_view_class.as_view(instance=self)(request)

    @classmethod
    def allowed_parent_page_models(cls):
        if not hasattr(cls, "parent_page_types"):
            return [
                model
                for model in apps.get_app_config(cls._meta.app_label).get_models()
                if issubclass(model, AbstractForum) and not model._meta.abstract
            ]
        return super().allowed_parent_page_models()

    @classmethod
    def allowed_subpage_models(cls):
        if not hasattr(cls, "subpage_types"):
            # We don't expect any subpages for topics by default.
            return []
        return super().allowed_subpage_models()


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

    content = QuillRichTextField(
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
