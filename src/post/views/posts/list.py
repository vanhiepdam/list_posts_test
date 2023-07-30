from django.views.generic import TemplateView


class ListPostView(TemplateView):
    template_name = "posts/list.html"
