from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import mixins
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import GenericViewSet

from apps.node_mgmt.filters.cloud_region import CloudRegionFilter
from apps.node_mgmt.serializers.cloud_region import CloudRegionSerializer, CloudRegionPartialUpdateSerializer
from apps.node_mgmt.models.cloud_region import CloudRegion
from drf_yasg import openapi


class CloudRegionViewSet(mixins.ListModelMixin,
                         mixins.UpdateModelMixin,
                         GenericViewSet):
    queryset = CloudRegion.objects.all()
    serializer_class = CloudRegionSerializer
    filterset_class = CloudRegionFilter
    filter_backends = [SearchFilter, OrderingFilter]  # 过滤后端
    search_fields = ['name', 'introduction']  # 搜索字段
    ordering_fields = ['name', 'created_at']  # 排序字段

    @swagger_auto_schema(
        operation_summary="获取云区域列表",
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description="可按名称或简介模糊搜索",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('ordering', openapi.IN_QUERY, description="排序字段(name,created_at)",
                              type=openapi.TYPE_STRING),
        ],
        tags=['CloudRegion']
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="部分更新云区域",
        tags=['CloudRegion'],
        request_body=CloudRegionPartialUpdateSerializer
    )
    def partial_update(self, request, *args, **kwargs):
        self.serializer_class = CloudRegionPartialUpdateSerializer
        return super().partial_update(request, *args, **kwargs)
