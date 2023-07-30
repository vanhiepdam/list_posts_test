from rest_framework.routers import DefaultRouter

from post.api.v1.posts.viewset import PostViewSetV1

router = DefaultRouter(trailing_slash=False)

router.register(r"^posts", PostViewSetV1, basename="posts")

urlpatterns = router.urls
