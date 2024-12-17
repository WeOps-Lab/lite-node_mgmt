from rest_framework import serializers

from apps.node_mgmt.models.cloud_region import CloudRegion
from apps.node_mgmt.models.env_variable import EnvVariable
from apps.node_mgmt.serializers.cloud_region import CloudRegionSerializer


class EnvVariableSerializer(serializers.ModelSerializer):
    cloud_region_id = serializers.PrimaryKeyRelatedField(queryset=CloudRegion.objects.all(), source='cloud_region')
    cloud_region = CloudRegionSerializer(read_only=True)

    class Meta:
        model = EnvVariable
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'cloud_region': {'read_only': True},
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

