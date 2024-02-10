import django_filters
from albums.models import *


class AlbumFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr= 'icontains')
    greater_than_or_equal_cost = django_filters.NumberFilter(field_name="cost",lookup_expr='gte')
    less_than_cost = django_filters.NumberFilter(field_name="cost",lookup_expr='lt')

    class Meta:
        model = Album
        fields = ['name', 'greater_than_or_equal_cost', 'less_than_cost']