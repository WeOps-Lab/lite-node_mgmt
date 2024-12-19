from apps.node_mgmt.models.sidecar import Node, CollectorConfiguration


class CollectorConfigurationService:
    @staticmethod
    def apply_to_node(node_id, collector_configuration_id):
        try:
            node = Node.objects.get(id=node_id)
            collector_configuration = CollectorConfiguration.objects.get(id=collector_configuration_id)
            if node.status.get('status') == 1:
                collector_configuration.nodes.add(node)
                collector_configuration.save()
                return {"success": True, "message": "采集器配置已成功应用到节点。"}
            else:
                return {"success": False, "message": "节点状态不活跃。"}
        except Node.DoesNotExist:
            return {"success": False, "message": "节点不存在。"}
        except CollectorConfiguration.DoesNotExist:
            return {"success": False, "message": "采集器配置不存在。"}
        except Exception as e:
            return {"success": False, "message": str(e)}
