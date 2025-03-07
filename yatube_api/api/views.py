# TODO:  Напишите свой вариант
from rest_framework import viewsets, permissions
from posts import models
from . import serializers
from rest_framework import pagination, mixins
from rest_framework import exceptions, status, filters
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


class PostViewSet(viewsets.ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    pagination_class = pagination.LimitOffsetPagination
    page_size = 5

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        post = self.get_object()
        if post is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if post.author == self.request.user:
            serializer.save(instance=post)
            return Response(status=status.HTTP_200_OK)
        raise exceptions.PermissionDenied()

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if post.author == self.request.user:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise exceptions.PermissionDenied()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(models.Post, pk=self.kwargs.get("post_id"))
        return models.Comment.objects.filter(post=post)

    def list(self, request, *args, **kwargs):
        comments = self.get_queryset()
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        comment = self.get_object()
        serializer = self.get_serializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        post = get_object_or_404(models.Post, pk=self.kwargs.get("post_id"))
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        comment = self.get_object()
        if comment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if self.request.user != comment.author:
            raise exceptions.PermissionDenied()

        serializer.save(instance=comment)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if self.request.user != comment.author:
            raise exceptions.PermissionDenied()

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Group.objects.all()
    serializer_class = serializers.GroupSerializer


class FollowViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    pagination_class = pagination.LimitOffsetPagination
    search_fields = ("following__username",)
    page_size = 5

    def get_queryset(self):
        return models.Follow.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = serializers.FollowSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        following_username = self.request.data.get("following")

        if not following_username:
            return Response(
                {"detail": "Field 'following' is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            following = models.User.objects.get(username=following_username)
        except models.User.DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if user == following:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if models.Follow.objects.filter(
        user=user,
        following=following).exists():
            return Response(
                {"detail": "You are already following this user."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        follow = models.Follow.objects.create(user=user, following=following)
        serializer = serializers.FollowSerializer(follow)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
