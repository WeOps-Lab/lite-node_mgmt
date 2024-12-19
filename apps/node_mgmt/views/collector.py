from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import GenericViewSet

from apps.node_mgmt.filters.collector import CollectorFilter
from apps.node_mgmt.models.sidecar import Collector
from apps.node_mgmt.serializers.collector import CollectorSerializer


class CollectorViewSet(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       GenericViewSet):
    queryset = Collector.objects.all()
    serializer_class = CollectorSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    filterset_class = CollectorFilter
    search_fields = ['name', 'introduction']
    ordering_fields = ['name', 'created_at']

    @swagger_auto_schema(
        operation_summary="获取采集器列表",
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description="按名称或简介模糊搜索", type=openapi.TYPE_STRING),
            openapi.Parameter('ordering', openapi.IN_QUERY, description="排序字段(name, created_at)",
                              type=openapi.TYPE_STRING),
        ],
        tags=['Collector']
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="获取采集器详情",
        tags=['Collector']
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
