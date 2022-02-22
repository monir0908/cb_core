from typing import Dict

from rest_framework import serializers

from user.models import User, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'merchant_rating_value', 'buyer_rating_value', 'settled_post')


class UserProfileSerializers(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = '__all__'

    def get_user_info(self, instance: UserProfile) -> Dict:
        return UserSerializer(instance.user).data


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'groups', 'user_permissions')
