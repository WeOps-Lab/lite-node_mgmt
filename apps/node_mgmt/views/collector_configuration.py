from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from apps.core.utils.web_utils import WebUtils
from apps.node_mgmt.models.sidecar import CollectorConfiguration
from apps.node_mgmt.serializers.collector_configuration import (
    CollectorConfigurationSerializer,
    CollectorConfigurationListSerializer,
    CollectorConfigurationCreateSerializer,
    CollectorConfigurationUpdateSerializer
)
from apps.node_mgmt.filters.collector_configuration import CollectorConfigurationFilter
from apps.node_mgmt.services.collector_configuration import CollectorConfigurationService


class CollectorConfigurationViewSet(viewsets.ModelViewSet):
    queryset = CollectorConfiguration.objects.all()
    serializer_class = CollectorConfigurationSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    filterset_class = CollectorConfigurationFilter
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']

    @swagger_auto_schema(
        operation_summary="获取指定云区域下的采集器配置列表",
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description="按名称模糊搜索", type=openapi.TYPE_STRING),
            openapi.Parameter('ordering', openapi.IN_QUERY, description="排序字段(name, created_at)",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('cloud_region_id', openapi.IN_QUERY, description="云区域ID", type=openapi.TYPE_STRING),
        ],
        tags=['CollectorConfiguration']
    )
    def list(self, request, *args, **kwargs):
        cloud_region_id = request.query_params.get('cloud_region_id')
        if cloud_region_id:
            self.queryset = self.queryset.filter(cloud_region_id=cloud_region_id)
        self.serializer_class = CollectorConfigurationListSerializer
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="获取采集器配置详情",
        tags=['CollectorConfiguration']
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="创建采集器配置",
        tags=['CollectorConfiguration']
    )
    def create(self, request, *args, **kwargs):
        self.serializer_class = CollectorConfigurationCreateSerializer
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="部分更新采集器配置",
        tags=['CollectorConfiguration']
    )
    def partial_update(self, request, *args, **kwargs):
        self.serializer_class = CollectorConfigurationUpdateSerializer
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="删除采集器配置",
        tags=['CollectorConfiguration']
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="批量删除采集器配置",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'ids': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING)
                ),
            },
            required=['ids']
        ),
        tags=['CollectorConfiguration']
    )
    @action(methods=['post'], detail=False, url_path='bulk_delete')
    def bulk_delete(self, request):
        ids = request.data.get('ids', [])
        if not ids:
            return WebUtils.response_success({"success": False, "message": "未提供要删除的ID列表。"})

        CollectorConfiguration.objects.filter(id__in=ids).delete()
        return WebUtils.response_success({"success": True, "message": "批量删除成功。"})

    @swagger_auto_schema(
        operation_summary="应用指定采集器配置到指定节点",
        manual_parameters=[
            openapi.Parameter('node_id', openapi.IN_PATH, description="节点ID", type=openapi.TYPE_STRING),
            openapi.Parameter('collector_configuration_id', openapi.IN_PATH, description="采集器配置ID",
                              type=openapi.TYPE_STRING),
        ],
        tags=['CollectorConfiguration']
    )
    @action(methods=['post'], detail=False,
            url_path='apply_to_node/(?P<node_id>[^/.]+)/(?P<collector_configuration_id>[^/.]+)')
    def apply_to_node(self, request, node_id, collector_configuration_id):
        result = CollectorConfigurationService.apply_to_node(node_id, collector_configuration_id)
        return WebUtils.response_success(result)
