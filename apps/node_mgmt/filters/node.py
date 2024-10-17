from django_filters import rest_framework as filters

from apps.node_mgmt.models.sidecar import Node


class NodeFilter(filters.FilterSet):
    node_id = filters.CharFilter(field_name='node_id', lookup_expr='exact')
    node_name = filters.CharFilter(field_name='node_name', lookup_expr='icontains')
    ip = filters.CharFilter(field_name='ip', lookup_expr='icontains')
    operating_system = filters.CharFilter(field_name='operating_system', lookup_expr='exact')

    class Meta:
        model = Node
        fields = ['node_id', 'node_name', 'ip', 'operating_system']
