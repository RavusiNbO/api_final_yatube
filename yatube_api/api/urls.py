from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register("posts", views.PostViewSet)
router.register(r"posts/(?P<post_id>\d+)/comments", views.CommentViewSet)
router.register("groups", views.GroupViewSet)
router.register("follow", views.FollowViewSet, basename="follow")


urlpatterns = [
    # JWT-эндпоинты, для управления JWT-токенами:
    path("", include("djoser.urls.jwt")),
    path("", include(router.urls)),
]
