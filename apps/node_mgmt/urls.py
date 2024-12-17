from rest_framework import routers

from apps.node_mgmt.views.cloud_region import CloudRegionViewSet
from apps.node_mgmt.views.env_variable import EnvVariableViewSet
# from apps.node_mgmt.views.node import NodeViewSet
from apps.node_mgmt.views.sidecar import SidecarViewSet, OpenSidecarViewSet

router = routers.DefaultRouter(trailing_slash=False)
# router.register(r"api/node", NodeViewSet, basename="node")
router.register(r"api/sidecar", SidecarViewSet, basename="sidecar")
router.register(r'api/cloud_region', CloudRegionViewSet, basename='cloud_region')
router.register(r'api/env_variable', EnvVariableViewSet, basename='env_variable')

router.register(r"open_api", OpenSidecarViewSet, basename="open_node")

urlpatterns = router.urls
