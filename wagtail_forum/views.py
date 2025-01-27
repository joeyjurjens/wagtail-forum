from django.views.generic import CreateView


class TopicCreateView(CreateView):
    fields = ["title", "content"]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
