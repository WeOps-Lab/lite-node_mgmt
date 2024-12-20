from apps.node_mgmt.models.sidecar import Node, CollectorConfiguration


class CollectorConfigurationService:
    @staticmethod
    def apply_to_node(node_id, collector_configuration_id):
        """将采集器配置应用到指定节点"""
        try:
            node = Node.objects.get(id=node_id)
            collector_configuration = CollectorConfiguration.objects.get(id=collector_configuration_id)
            collector = collector_configuration.collector

            # 检查节点是否已经有该配置文件对应的采集器关联的配置文件
            existing_configurations = node.collectorconfiguration_set.filter(collector=collector)
            if existing_configurations.exists():
                # 覆盖现有配置文件
                for config in existing_configurations:
                    config.nodes.remove(node)

            # 添加新的配置文件
            collector_configuration.nodes.add(node)
            collector_configuration.save()
            return {"success": True, "message": "采集器配置已成功应用到节点。"}
        except Exception as e:
            return {"success": False, "message": str(e)}
