import json

from django.forms import widgets, Media
from django.utils.functional import cached_property

from .settings import QUILL_EDITOR_CONFIG


class QuillRichTextArea(widgets.HiddenInput):
    template_name = "wagtail_forum/widgets/quill.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["options"] = json.dumps(QUILL_EDITOR_CONFIG)
        return context

    @cached_property
    def media(self):
        return Media(
            js=["wagtail_forum/js/quill.js"],
            css={"all": ["wagtail_forum/css/wagtail-forum.css"]},
        )
