from django_filters import rest_framework as filters
from apps.node_mgmt.models.cloud_region import CloudRegion
from apps.node_mgmt.models.env_variable import EnvVariable


class CloudRegionFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    introduction = filters.CharFilter(field_name='introduction', lookup_expr='icontains')

    class Meta:
        model = CloudRegion
        fields = ['name', 'introduction']
