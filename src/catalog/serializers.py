from base.serializers import BaseModelSerializer

from catalog.models import Category, Genre


class CategoryAdminSerializer(BaseModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GenreAdminSerializer(BaseModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class CategoryUserSerializer(BaseModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreUserSerializer(BaseModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')

