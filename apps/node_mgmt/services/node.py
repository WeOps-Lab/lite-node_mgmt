from apps.node_mgmt.models.sidecar import Node, Collector, CollectorConfiguration, Action
from apps.node_mgmt.serializers.node import NodeSerializer


class NodeService:
    @staticmethod
    def node_list(queryset):
        """获取节点列表，并补充采集器名称和采集器配置名称"""
        nodes = []
        for node in queryset:
            node_data = NodeSerializer(node).data
            if 'collectors' not in node_data['status']:
                continue
            for collector in node_data['status']['collectors']:
                try:
                    collector_obj = Collector.objects.get(id=collector['collector_id'])
                    collector['collector_name'] = collector_obj.name
                except Collector.DoesNotExist:
                    collector['collector_name'] = None

                try:
                    configuration_obj = CollectorConfiguration.objects.get(id=collector['configuration_id'])
                    collector['configuration_name'] = configuration_obj.name
                except CollectorConfiguration.DoesNotExist:
                    collector['configuration_name'] = None
            nodes.append(node_data)

        return nodes


    @staticmethod
    def batch_binding_node_configuration(node_ids, collector_configuration_id):
        """批量绑定配置到多个节点"""
        try:
            collector_configuration = CollectorConfiguration.objects.get(id=collector_configuration_id)
            collector = collector_configuration.collector

            for node_id in node_ids:
                try:
                    node = Node.objects.get(id=node_id)

                    # 检查节点是否已经有该配置文件对应的采集器关联的配置文件
                    existing_configurations = node.collectorconfiguration_set.filter(collector=collector)
                    if existing_configurations.exists():
                        # 覆盖现有配置文件
                        for config in existing_configurations:
                            config.nodes.remove(node)

                    # 添加新的配置文件
                    collector_configuration.nodes.add(node)
                except Node.DoesNotExist:
                    continue  # 跳过不存在的节点

            collector_configuration.save()
            return {"success": True, "message": "采集器配置已成功应用到所有节点。"}
        except Exception as e:
            return {"success": False, "message": str(e)}

    @staticmethod
    def batch_operate_node_collector(node_ids, collector_id, operation):
        """批量操作节点采集器"""
        actions = []
        for node_id in node_ids:
            try:
                node = Node.objects.get(id=node_id)
                action_data = {
                    "collector_id": collector_id,
                    "properties": {operation: True}
                }
                action, created = Action.objects.get_or_create(node=node)
                action.action.append(action_data)
                action.save()
                actions.append(action)
            except Node.DoesNotExist:
                continue  # 跳过不存在的节点

        return {"success": True, "message": "操作成功。"}
