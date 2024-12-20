from django_filters import rest_framework as filters
from apps.node_mgmt.models.sidecar import SidecarEnv


class SidecarEnvFilter(filters.FilterSet):
    key = filters.CharFilter(field_name='key', lookup_expr='exact')
    cloud_region_id = filters.NumberFilter(field_name='cloud_region_id', lookup_expr='exact')

    class Meta:
        model = SidecarEnv
        fields = ['key', 'cloud_region_id']
