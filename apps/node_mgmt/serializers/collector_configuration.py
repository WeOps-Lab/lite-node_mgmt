from rest_framework import serializers

from apps.node_mgmt.models.cloud_region import CloudRegion
from apps.node_mgmt.models.sidecar import CollectorConfiguration, Node, Collector


class CollectorConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectorConfiguration
        fields = '__all__'


class CollectorConfigurationListSerializer(serializers.ModelSerializer):
    collector = serializers.PrimaryKeyRelatedField(queryset=Collector.objects.all())
    nodes = serializers.PrimaryKeyRelatedField(queryset=Node.objects.all(), many=True)
    node_count = serializers.SerializerMethodField()

    class Meta:
        model = CollectorConfiguration
        fields = ['id', 'name', 'config_template', 'operating_system', 'collector', 'nodes', 'node_count']

    def get_node_count(self, obj):
        return obj.nodes.count()


class CollectorConfigurationCreateSerializer(serializers.ModelSerializer):
    cloud_region_id = serializers.PrimaryKeyRelatedField(queryset=CloudRegion.objects.all(), source='cloud_region')
    collector_id = serializers.PrimaryKeyRelatedField(queryset=Collector.objects.all(), source='collector')

    class Meta:
        model = CollectorConfiguration
        fields = ['name', 'config_template', 'operating_system', 'collector_id', 'cloud_region_id']


class CollectorConfigurationUpdateSerializer(serializers.ModelSerializer):
    collector_id = serializers.PrimaryKeyRelatedField(queryset=Collector.objects.all(), source='collector')

    class Meta:
        model = CollectorConfiguration
        fields = ['name', 'config_template', 'operating_system', 'collector_id']
