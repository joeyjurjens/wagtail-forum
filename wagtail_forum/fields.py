from django.db import models

from .widgets import QuillRichTextArea


class QuillRichTextField(models.TextField):
    def formfield(self, **kwargs):
        return super().formfield(widget=QuillRichTextArea, **kwargs)
