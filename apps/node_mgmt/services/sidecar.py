import hashlib
from django.core.cache import cache
from django.http import JsonResponse
from django.utils.http import quote_etag

from apps.node_mgmt.constants import L_INSTALL_DOWNLOAD_URL, L_SIDECAR_DOWNLOAD_URL, W_SIDECAR_DOWNLOAD_URL
from apps.node_mgmt.models.sidecar import Node, Collector, CollectorConfiguration, Action, NodeCollectorConfiguration


class Sidecar:

    @staticmethod
    def generate_etag(data):
        """根据Collector列表生成ETag"""
        return quote_etag(hashlib.md5(data.encode('utf-8')).hexdigest())

    @staticmethod
    def get_version():
        """获取版本信息"""
        return JsonResponse({"version": "4.0.0"})

    @staticmethod
    def get_collectors(request):
        """获取采集器列表"""

        # 获取客户端的 ETag
        if_none_match = request.headers.get('If-None-Match')

        # 从缓存中获取采集器的 ETag
        cached_etag = cache.get('collectors_etag')

        # 如果缓存的 ETag 存在且与客户端的相同，则返回 304 Not Modified
        if cached_etag and cached_etag == if_none_match:
            return JsonResponse(status=304, data={}, headers={'ETag': cached_etag})

        # 从数据库获取采集器列表
        collectors = list(Collector.objects.values())

        for collector in collectors:
            collector.update(
                id=collector.pop('collector_id'),
                name=collector.pop('collector_name'),
                node_operating_system=collector.pop('operating_system'),
            )

        # 生成新的 ETag
        _collectors = JsonResponse(collectors, safe=False).content
        new_etag = Sidecar.generate_etag(_collectors.decode('utf-8'))

        # 更新缓存中的 ETag
        cache.set('collectors_etag', new_etag)

        # 返回采集器列表和新的 ETag
        return JsonResponse({'collectors': collectors}, headers={'ETag': new_etag})

    @staticmethod
    def update_node_client(request, node_id):
        """更新sidecar客户端信息"""

        # 从请求体中获取数据
        request_data = dict(
            node_id=node_id,
            node_name=request.data.get("node_name", ""),
            **request.data.get("node_details", {}),
        )

        # 更新或创建Sidecar信息
        new_obj, _ = Node.objects.update_or_create(node_id=node_id, defaults=request_data)

        # 获取客户端发送的ETag
        if_none_match = request.headers.get('If-None-Match')

        # 从缓存中获取node的ETag
        cached_etag = cache.get(f"node_etag_{node_id}")

        # 如果缓存的ETag存在且与客户端的相同，则返回304 Not Modified
        if cached_etag and cached_etag == if_none_match:
            return JsonResponse(status=304, data={}, headers={'ETag': cached_etag})

        # 构造响应数据
        response_data = dict(
                configuration={"update_interval": 5, "send_status": True},    # 配置信息, 60s更新一次
                configuration_override=True,    # 是否覆盖配置
                actions=[],   # 采集器状态
                assignments=[],   # 采集器配置
            )
        action_obj = Action.objects.filter(node_id=node_id).first()
        if action_obj:
            response_data.update(actions=action_obj.action)
            action_obj.delete()
        assignments = NodeCollectorConfiguration.objects.filter(node_id=node_id)
        if assignments:
            response_data.update(
                assignments=[{"collector_id": i.collector_id, "configuration_id": i.config_id} for i in assignments])

        # 生成新的ETag
        _response_data = JsonResponse(response_data).content
        new_etag = Sidecar.generate_etag(_response_data.decode('utf-8'))
        # 更新缓存中的ETag
        cache.set(f"node_etag_{node_id}", new_etag)

        # 返回响应
        return JsonResponse(status=202, data=response_data, headers={'ETag': new_etag})

    @staticmethod
    def get_node_config(request, node_id, configuration_id):
        """获取节点配置信息"""

        # 获取客户端发送的 ETag
        if_none_match = request.headers.get('If-None-Match')

        # 从缓存中获取配置的 ETag
        cached_etag = cache.get(f"configuration_etag_{configuration_id}")

        # 对比客户端的 ETag 和缓存的 ETag
        if cached_etag and cached_etag == if_none_match:
            return JsonResponse(status=304, data={}, headers={'ETag': cached_etag})

        # 从数据库获取节点信息
        node = NodeCollectorConfiguration.objects.filter(node_id=node_id, config_id=configuration_id).first()
        if not node:
            return JsonResponse(status=404, data={}, manage="Node collector Configuration not found")

        # 从数据库获取配置信息
        configuration = CollectorConfiguration.objects.filter(config_id=configuration_id).first()
        if not configuration:
            return JsonResponse(status=404, data={}, manage="Configuration not found")
        configuration = dict(
            id=configuration.config_id,
            collector_id=configuration.collector.collector_id,
            name=configuration.config_name,
            template=configuration.config_template,
        )
        # 生成新的 ETag
        _configuration = JsonResponse(configuration).content
        new_etag = Sidecar.generate_etag(_configuration.decode('utf-8'))

        # 更新缓存中的 ETag
        cache.set(f"configuration_etag_{configuration_id}", new_etag)

        # 返回配置信息和新的 ETag
        return JsonResponse(configuration, headers={'ETag': new_etag})

    # def get_installation_steps(self):
    #     """获取安装步骤"""
    #     local_host = LOCAL_HOST
    #     local_api_token = ""
    #
    #     if self.node.os_type == LINUX_OS:
    #         return self.linux_step(self.node.node_id, local_api_token, local_host)
    #     elif self.node.os_type == WINDOWS_OS:
    #         return self.windows_step(self.node.node_id, local_api_token, local_host)

    def windows_step(self, node_id, gl_token, gl_host):
        """windows安装步骤"""

        return [
            {
                "title": "下载安装包",
                "content": "下载安装包",
                "download_url": W_SIDECAR_DOWNLOAD_URL,
            },
            {
                "title": "创建以下目录",
                "content": "c:/gse",
            },
            {
                "title": "执行安装脚本，在指定目录下安装控制器和探针",
                "content": r'.\install_sidecar.bat "{}" "{}" "{}"'.format(node_id, gl_token, gl_host),
            },
        ]

    def linux_step(self, node_id, gl_token, gl_host):
        """linux安装步骤"""

        params = [L_INSTALL_DOWNLOAD_URL, node_id, gl_token, gl_host, L_SIDECAR_DOWNLOAD_URL]
        return [
            {
                "title": "下载安装包",
                "content": 'curl -sSL {}|bash -s - -n "{}" -t "{}" -s "{}" -d "{}"'.format(*params),
            },
        ]
