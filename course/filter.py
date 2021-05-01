from django_filters import rest_framework as filters
from .models import CourseModel


class CourseFilter(filters.FilterSet):
    old_price = filters.NumberFilter(field_name='old_price',lookup_expr='contains')
    new_price = filters.NumberFilter(field_name='new_price', lookup_expr='contains')
    status = filters.NumberFilter(field_name='status', lookup_expr='contains')
    description = filters.CharFilter(field_name='description', lookup_expr='contains')
    title = filters.CharFilter(field_name='title', lookup_expr='contains')
    user = filters.CharFilter(field_name='user_id', lookup_expr='exact')
    type = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = CourseModel
        fields = {
            'title',
            'new_price',
            'new_price',
            'description',
            'status',
            'user_id',
            'type',
        }

    def type_filter(self, queryset, name, value):
        return queryset.filter(type=value)
