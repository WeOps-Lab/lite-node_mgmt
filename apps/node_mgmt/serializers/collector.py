from rest_framework import serializers
from apps.node_mgmt.models.sidecar import Collector


class CollectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collector
        fields = ['id', 'name', 'node_operating_system', 'introduction', 'details', 'created_at', 'updated_at']

