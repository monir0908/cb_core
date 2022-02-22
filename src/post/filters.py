import django_filters

from post.models import Post


class PostFilters(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name='username', lookup_expr='exact')
    username__icontains = django_filters.CharFilter(field_name='username', lookup_expr='icontains')
    title = django_filters.CharFilter(field_name='title', lookup_expr='istartswith')
    quantity = django_filters.RangeFilter(field_name='quantity')
    size_type = django_filters.CharFilter(field_name='size_type', lookup_expr='icontains')
    size_inch_max = django_filters.NumberFilter(field_name='size_inch_max', lookup_expr='gte')
    size_cm_max = django_filters.NumberFilter(field_name='size_cm_max', lookup_expr='gte')
    max_color_variety = django_filters.NumberFilter(field_name='max_color_variety', lookup_expr='gte')
    size_inch_min = django_filters.NumberFilter(field_name='size_inch_min', lookup_expr='lte')
    min_color_variety = django_filters.NumberFilter(field_name='min_color_variety', lookup_expr='lte')
    size_cm_min = django_filters.NumberFilter(field_name='size_cm_min', lookup_expr='lte')
    status = django_filters.CharFilter(field_name='status', lookup_expr='exact')
    genre__slug = django_filters.CharFilter(lookup_expr='exact')
    category__slug = django_filters.CharFilter(lookup_expr='exact')
    unit = django_filters.CharFilter(field_name='unit', lookup_expr='exact')
    unit_price = django_filters.RangeFilter(field_name='unit_price')
    minimum_order_quantity = django_filters.RangeFilter(field_name='minimum_order_quantity')
    identifier = django_filters.CharFilter(field_name='identifier', lookup_expr='exact')
    created_by__userprofile__company_name = django_filters.CharFilter(lookup_expr='istartswith')
    postsize__value = django_filters.CharFilter(lookup_expr='in')

    class Meta:
        model = Post
        fields = ('username', 'title', 'quantity', 'size_type', 'size_inch_max', 'size_inch_min',
                  'size_cm_max', 'size_cm_min', 'genre', 'category', 'unit', 'unit_price', 'minimum_order_quantity',
                  'min_color_variety', 'identifier', 'max_color_variety', 'min_color_variety', 'created_by')
        order_by_field = ('total_interest', 'created_at')
