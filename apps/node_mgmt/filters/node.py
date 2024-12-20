from django_filters import rest_framework as filters

from apps.node_mgmt.models.sidecar import Node


class NodeFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    ip = filters.CharFilter(field_name='ip', lookup_expr='icontains')
    operating_system = filters.CharFilter(field_name='operating_system', lookup_expr='exact')
    cloud_region_id = filters.CharFilter(field_name='cloud_region_id', lookup_expr='exact')

    class Meta:
        model = Node
        fields = ['name', 'ip', 'operating_system', 'cloud_region_id']
