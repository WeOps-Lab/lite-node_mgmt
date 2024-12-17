from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.node_mgmt.filters.env_variable import EnvVariableFilter
from apps.node_mgmt.models.env_variable import EnvVariable
from apps.node_mgmt.serializers.env_variable import EnvVariableSerializer


class EnvVariableViewSet(ModelViewSet):
    queryset = EnvVariable.objects.all()
    serializer_class = EnvVariableSerializer
    filterset_class = EnvVariableFilter
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['key', 'description']
    ordering_fields = ['key', 'created_at']

    @swagger_auto_schema(
        operation_description="获取环境变量列表",
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description="按名称或描述模糊搜索", type=openapi.TYPE_STRING),
            openapi.Parameter('ordering', openapi.IN_QUERY, description="排序字段(key,created_at)", type=openapi.TYPE_STRING),
        ],
        responses={200: EnvVariableSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="获取环境变量详情",
        responses={200: EnvVariableSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="创建环境变量",
        request_body=EnvVariableSerializer,
        responses={200: EnvVariableSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="更新环境变量",
        request_body=EnvVariableSerializer,
        responses={200: EnvVariableSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="部分更新环境变量",
        request_body=EnvVariableSerializer,
        responses={200: EnvVariableSerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="删除环境变量",
        responses={200: EnvVariableSerializer()}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        method='post',
        operation_description="批量删除环境变量",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'ids': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING))
            },
            required=['ids']
        ),
        responses={200: openapi.Response('删除成功')}
    )
    @action(detail=False, methods=['post'], url_path='bulk_delete')
    def bulk_delete(self, request):
        ids = request.data.get('ids', [])
        if not ids:
            return Response({'error': '没有提供id'}, status=status.HTTP_400_BAD_REQUEST)
        deleted_count, _ = EnvVariable.objects.filter(id__in=ids).delete()
        return Response({'成功删除数量': deleted_count}, status=status.HTTP_200_OK)
