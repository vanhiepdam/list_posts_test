from django.urls import path

from post.views.posts.list import ListPostView

urlpatterns = [
    path("", ListPostView.as_view()),
]
