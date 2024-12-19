from django_filters import rest_framework as filters
from apps.node_mgmt.models.sidecar import CollectorConfiguration


class CollectorConfigurationFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    collector_id = filters.NumberFilter(field_name='collector_id', lookup_expr='exact')
    cloud_region_id = filters.NumberFilter(field_name='cloud_region_id', lookup_expr='exact')

    class Meta:
        model = CollectorConfiguration
        fields = ['name', 'collector_id', 'cloud_region_id']
