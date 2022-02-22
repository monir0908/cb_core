from rest_framework.serializers import SerializerMethodField, ModelSerializer
from rest_framework import serializers
from user.serializers import UserSerializer
from .models import BaseModel
from django.contrib.auth import get_user_model

User = get_user_model()


class ReadWriteSerializerMethodField(SerializerMethodField):
    """
    Default SerializerMethodField in drf is read only.
    This method field class supports both read and write
    """

    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name
        kwargs["source"] = "*"
        super(SerializerMethodField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        return {f'{self.field_name}_id': data}


class BaseModelSerializer(ModelSerializer):
    created_by = ReadWriteSerializerMethodField()
    updated_by = UserSerializer(read_only=True, many=False)
    updated_by_id = serializers.PrimaryKeyRelatedField(source='updated_by', write_only=True,
                                                       queryset=User.objects.all(), allow_null=True, required=False)

    def get_created_by(self, obj):
        return UserSerializer(instance=obj.created_by).data

    class Meta:
        model = BaseModel
        abstract = True
