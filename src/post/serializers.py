from typing import Dict, List

from rest_framework import serializers

from post.models import Post, PostInterest, PostSize, PostBookmark, PostComment, SettlePost, PostConfig
from catalog.serializers import CategoryUserSerializer
from base.serializers import BaseModelSerializer, ReadWriteSerializerMethodField
from user.serializers import UserSerializer


class PostSizesLiteSerializer(BaseModelSerializer):
    class Meta:
        model = PostSize
        fields = ('value',)


class PostConfigSerializer(BaseModelSerializer):
    class Meta:
        model = PostConfig
        fields = '__all__'


class PostLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'slug')


class PostSerializer(BaseModelSerializer):
    category = ReadWriteSerializerMethodField()
    genre = ReadWriteSerializerMethodField()
    sizes = serializers.SerializerMethodField()

    def get_category(self, obj: Post) -> Dict:
        return CategoryUserSerializer(obj.category).data

    def get_genre(self, obj: Post) -> Dict:
        return CategoryUserSerializer(obj.genre).data

    def get_sizes(self, obj: Post) -> List:
        if obj.postsize_set.all():
            return PostSizesLiteSerializer(instance=obj.postsize_set.all(), many=True).data
        return []

    class Meta:
        model = Post
        fields = '__all__'


class PostInterestSerializer(BaseModelSerializer):
    post = ReadWriteSerializerMethodField()

    class Meta:
        model = PostInterest
        fields = '__all__'

    def get_post(self, instance: PostInterest) -> Dict:
        return PostLiteSerializer(instance.post).data


class PostBookMarkSerializer(BaseModelSerializer):
    post = ReadWriteSerializerMethodField()

    class Meta:
        model = PostBookmark
        fields = '__all__'

    def get_post(self, instance: PostBookmark) -> Dict:
        return PostLiteSerializer(instance.post).data


class PostCommentSerializer(BaseModelSerializer):
    post = ReadWriteSerializerMethodField()

    class Meta:
        model = PostComment
        fields = '__all__'

    def get_post(self, instance: PostComment) -> Dict:
        return PostLiteSerializer(instance.post).data


class PostSettleSerializer(BaseModelSerializer):
    post = ReadWriteSerializerMethodField()
    settled_with = ReadWriteSerializerMethodField()

    class Meta:
        model = SettlePost
        fields = '__all__'

    def get_post(self, instance: SettlePost) -> Dict:
        return PostLiteSerializer(instance.post).data

    def get_settled_with(self, instance: SettlePost) -> Dict:
        return UserSerializer(instance.settled_with).data
