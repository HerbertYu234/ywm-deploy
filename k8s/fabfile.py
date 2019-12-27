# k8s deployment fabfile
# coding: utf8
from __future__ import print_function

import os

from fabric.api import *

profile = "prod"
print("当前部署环境:%s" % profile)


def _get_resource_type(restype):
    """
    获取资源类型
    :param restype: 资源类型字符串
    :return: normalized resource type
    """
    if restype in ['cm', "configmap"]:
        return "cm"
    elif restype in ['dp', 'deploy','deployment']:
        return "deploy"
    else:
        raise Exception("未能识别的资源类型")


@with_settings(warn_only=True)
def _apply(restype, **kwargs):
    """
    调用kubectl apply ...
    :param restype: 资源类型
    :param kwargs: keys: name[必填],replica...
    """
    delete = "delete" in kwargs
    local("kubetpl render %s.yaml -i %s.env %s | kubectl %s -f- "
          % (_get_resource_type(restype), profile,
             " ".join(["-s %s=%s" % (item[0], item[1]) for item in tuple(kwargs.items())]),
             delete and "delete" or "apply"))

    # 如果是删除, 那么删除后还需要apply一下
    if delete:
        kwargs.pop("delete")
        _apply(restype=restype, **kwargs)


def configmap():
    """
    k8s apply configmap
    """
    return _apply(restype="configmap")


def deploy(**kwargs):
    """
    k8s apply deployment
    fab deploy:name=oms,delete=1
    :return:
    """
    return _apply(restype="deployment", **kwargs)
