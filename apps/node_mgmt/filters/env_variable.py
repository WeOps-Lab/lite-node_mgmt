from django_filters import rest_framework as filters
from apps.node_mgmt.models.env_variable import EnvVariable


class EnvVariableFilter(filters.FilterSet):
    key = filters.CharFilter(field_name='key', lookup_expr='exact')
    value = filters.CharFilter(field_name='value', lookup_expr='icontains')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')
    cloud_region_id = filters.NumberFilter(field_name='cloud_region_id', lookup_expr='exact')

    class Meta:
        model = EnvVariable
        fields = ['key', 'value', 'description', 'cloud_region_id']
