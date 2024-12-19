from rest_framework import serializers

from apps.node_mgmt.models.cloud_region import CloudRegion
from apps.node_mgmt.models.env_variable import EnvVariable
from apps.node_mgmt.serializers.cloud_region import CloudRegionSerializer


class EnvVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnvVariable
        fields = ['id', 'key', 'value', 'description']


class EnvVariableCreateSerializer(serializers.ModelSerializer):
    cloud_region_id = serializers.PrimaryKeyRelatedField(queryset=CloudRegion.objects.all(), source='cloud_region')

    class Meta:
        model = EnvVariable
        fields = ['key', 'value', 'description', 'cloud_region_id']


class EnvVariableUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnvVariable
        fields = ['key', 'value', 'description']
