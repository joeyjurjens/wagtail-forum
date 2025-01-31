from django.http import HttpResponseRedirect
from django.views.generic import CreateView, View


class TopicCreateView(CreateView):
    fields = ["title", "content"]
    # Passed in as_view.
    forum = None

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["page"] = self.forum
        return ctx

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["title"].help_text = ""
        form.fields["content"].help_text = ""
        return form

    def form_valid(self, form):
        """
        Since the model is a page model, the creation is a little different than a regular model.
        """
        # ToDo: Make forum creation require logged in user.
        topic_page = self.model(created_by=self.request.user)
        for field in form.cleaned_data:
            setattr(topic_page, field, form.cleaned_data[field])

        created_page = self.forum.add_child(instance=topic_page)
        return HttpResponseRedirect(created_page.get_url(request=self.request))


class TopicEditView(View):
    pass


class TopicReplyView(View):
    pass


class TopicReactView(View):
    pass
