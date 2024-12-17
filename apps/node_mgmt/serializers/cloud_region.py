from rest_framework import serializers
from apps.node_mgmt.models.cloud_region import CloudRegion


class CloudRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloudRegion
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
