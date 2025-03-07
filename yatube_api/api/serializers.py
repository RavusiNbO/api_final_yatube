from rest_framework import serializers
from rest_framework.relations import SlugRelatedField, PrimaryKeyRelatedField


from posts.models import Comment, Post, Group, Follow


class GroupSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = "__all__"
        model = Group


class PostSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    author = SlugRelatedField(slug_field="username", read_only=True)
    text = serializers.CharField()
    pub_date = serializers.DateTimeField(read_only=True)
    image = serializers.ImageField(required=False)
    group = PrimaryKeyRelatedField(
        queryset=Group.objects.all(), required=False, allow_null=True
    )

    class Meta:
        fields = "__all__"
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field="username", read_only=True)
    text = serializers.CharField()

    class Meta:
        fields = "__all__"
        read_only_fields = ("post", "created")
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(read_only=True, slug_field="username")
    following = SlugRelatedField(
        queryset=Follow.objects.all(),
        slug_field="username")

    class Meta:
        fields = ("user", "following")
        model = Follow
