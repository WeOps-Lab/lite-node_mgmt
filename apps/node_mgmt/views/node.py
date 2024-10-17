from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from apps.core.utils.web_utils import WebUtils
from apps.node_mgmt.constants import SIDECAR_STATUS_ENUM
from apps.node_mgmt.filters.node import NodeFilter
from apps.node_mgmt.models.sidecar import Node
from config.drf.pagination import CustomPageNumberPagination


class NodeViewSet(mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = Node.objects.all().order_by("-created_at")
    filterset_class = NodeFilter
    pagination_class = CustomPageNumberPagination

    @swagger_auto_schema(
        operation_id="node_list",
        operation_description="节点列表",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="node_del",
        operation_description="删除节点",
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return WebUtils.response_success()

    @swagger_auto_schema(
        operation_id="node_enum",
        operation_description="节点管理的枚举值",
    )
    @action(methods=["get"], detail=False, url_path=r"enum")
    def enum(self, request, *args, **kwargs):
        return WebUtils.response_success(dict(sidecar_status=SIDECAR_STATUS_ENUM))
