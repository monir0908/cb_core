import django_filters

from user.models import User


class UserFilters(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name='username', lookup_expr='exact')
    merchant_rating_value = django_filters.RangeFilter(field_name='merchant_rating_value')
    buyer_rating_value = django_filters.RangeFilter(field_name='buyer_rating_value')
    settled_post = django_filters.RangeFilter(field_name='settled_post')

    class Meta:
        model = User
        fields = ('username', )
        order_by_field = ('merchant_rating_value', 'buyer_rating_value', 'settled_post')
