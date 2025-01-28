from django.apps import AppConfig
from django.conf import settings


class WagtailForumAPIAppConfig(AppConfig):
    name = "wagtail_forum.contrib.api"
    label = "wagtail_forum_api"
    verbose_name = "Wagtail Forum API"
    default_auto_field = getattr(
        settings, "DEFAULT_AUTO_FIELD", "django.db.models.AutoField"
    )
