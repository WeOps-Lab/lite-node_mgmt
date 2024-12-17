from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from drf_yasg.utils import swagger_auto_schema

from apps.node_mgmt.filters.cloud_region import CloudRegionFilter
from apps.node_mgmt.serializers.cloud_region import CloudRegionSerializer
from apps.node_mgmt.models.cloud_region import CloudRegion
from drf_yasg import openapi


class CloudRegionViewSet(ModelViewSet):
    queryset = CloudRegion.objects.all()
    serializer_class = CloudRegionSerializer
    filterset_class = CloudRegionFilter
    filter_backends = [SearchFilter, OrderingFilter]  # 过滤后端
    search_fields = ['name', 'introduction']  # 搜索字段
    ordering_fields = ['name', 'created_at']  # 排序字段

    @swagger_auto_schema(
        operation_description="获取云区域列表",
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description="可按名称或简介模糊搜索",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('ordering', openapi.IN_QUERY, description="排序时要使用哪个字段(name,created_at)",
                              type=openapi.TYPE_STRING),
        ],
        responses={200: CloudRegionSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="获取云区域详情",
        responses={200: CloudRegionSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="创建云区域",
        request_body=CloudRegionSerializer,
        responses={200: CloudRegionSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="更新云区域",
        request_body=CloudRegionSerializer,
        responses={200: CloudRegionSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="部分更新云区域",
        request_body=CloudRegionSerializer,
        responses={200: CloudRegionSerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="删除云区域",
        responses={200: CloudRegionSerializer()}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
