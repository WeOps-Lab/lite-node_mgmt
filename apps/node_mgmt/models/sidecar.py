from django.db import models
from django.db.models import JSONField

from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo


class Node(TimeInfo, MaintainerInfo):

    id = models.CharField(primary_key=True, max_length=100, verbose_name="节点ID")
    name = models.CharField(max_length=100, verbose_name="节点名称")
    ip = models.CharField(max_length=30, verbose_name="IP地址")
    operating_system = models.CharField(max_length=50, default="", verbose_name="操作系统类型")
    collector_configuration_directory = models.CharField(max_length=200, verbose_name="采集器配置目录")
    metrics = JSONField(default=dict, verbose_name="指标")
    status = JSONField(default=dict, verbose_name="状态")
    tags = JSONField(default=list, verbose_name="标签")
    log_file_list = JSONField(default=list, verbose_name="日志文件列表")

    class Meta:
        verbose_name = "节点信息"
        db_table = "node"


class Collector(TimeInfo, MaintainerInfo):

    id = models.CharField(primary_key=True, max_length=100, verbose_name="采集器ID")
    name = models.CharField(max_length=100, verbose_name="采集器名称")
    service_type = models.CharField(max_length=100, verbose_name="服务类型")
    node_operating_system = models.CharField(max_length=50, default="", verbose_name="节点操作系统类型")
    executable_path = models.CharField(max_length=200, verbose_name="可执行文件路径")
    execute_parameters = models.CharField(max_length=200, verbose_name="执行参数")
    validation_parameters = models.CharField(max_length=200, verbose_name="验证参数")

    class Meta:
        verbose_name = "采集器信息"
        db_table = "collector"


class CollectorConfiguration(TimeInfo, MaintainerInfo):

    id = models.CharField(primary_key=True, max_length=100, verbose_name="配置ID")
    name = models.CharField(max_length=100, verbose_name="配置名称")
    config_template = models.TextField(verbose_name="配置模板")
    collector = models.ForeignKey(Collector, on_delete=models.CASCADE, verbose_name="采集器")
    nodes = models.ManyToManyField(Node, verbose_name="节点")

    class Meta:
        verbose_name = "采集器配信息"
        db_table = "collector_configuration"


class Action(TimeInfo, MaintainerInfo):

    node = models.ForeignKey(Node, on_delete=models.CASCADE, verbose_name="节点")
    action = JSONField(default=list, verbose_name="操作")

    class Meta:
        verbose_name = "操作信息"
        db_table = "action"
