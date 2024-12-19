from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets, mixins
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.viewsets import GenericViewSet

from apps.core.utils.web_utils import WebUtils
from apps.node_mgmt.filters.env_variable import EnvVariableFilter
from apps.node_mgmt.models.env_variable import EnvVariable
from apps.node_mgmt.serializers.env_variable import EnvVariableSerializer, EnvVariableCreateSerializer, \
    EnvVariableUpdateSerializer


class EnvVariableViewSet(mixins.CreateModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    queryset = EnvVariable.objects.all()
    serializer_class = EnvVariableSerializer
    filterset_class = EnvVariableFilter
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['key', 'description']
    ordering_fields = ['key', 'created_at']

    @swagger_auto_schema(
        operation_summary="获取指定云区域的环境变量列表",
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description="按名称或描述模糊搜索", type=openapi.TYPE_STRING),
            openapi.Parameter('ordering', openapi.IN_QUERY, description="排序字段(key,created_at)",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('cloud_region_id', openapi.IN_QUERY, description="云区域ID", type=openapi.TYPE_STRING),
        ],
        tags=['EnvVariable']
    )
    def list(self, request, *args, **kwargs):
        cloud_region_id = request.query_params.get('cloud_region_id')
        if cloud_region_id:
            self.queryset = self.queryset.filter(cloud_region_id=cloud_region_id)
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="创建环境变量",
        tags=['EnvVariable']
    )
    def create(self, request, *args, **kwargs):
        self.serializer_class = EnvVariableCreateSerializer
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="部分更新环境变量",
        tags=['EnvVariable']
    )
    def partial_update(self, request, *args, **kwargs):
        self.serializer_class = EnvVariableUpdateSerializer
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="删除环境变量",
        tags=['EnvVariable']
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        method='post',
        operation_summary="批量删除环境变量",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'ids': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_INTEGER))
            },
            required=['ids']
        ),
        tags=['EnvVariable']
    )
    @action(detail=False, methods=['post'], url_path='bulk_delete')
    def bulk_delete(self, request):
        ids = request.data.get('ids', [])
        if not ids:
            return WebUtils.response_success({'success': False, 'message': '没有提供id'})
        deleted_count, _ = EnvVariable.objects.filter(id__in=ids).delete()
        return WebUtils.response_success({'success': True, 'message': f'成功删除数量: {deleted_count}'})
