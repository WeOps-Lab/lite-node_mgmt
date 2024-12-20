from django_filters import rest_framework as filters
from apps.node_mgmt.models.sidecar import Collector


class CollectorFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    node_operating_system = filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = Collector
        fields = ['name', 'node_operating_system']
