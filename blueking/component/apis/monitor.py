# -*- coding: utf-8 -*-
from ..base import ComponentAPI


class CollectionsMONITOR(object):
    """Collections of MONITOR APIS"""

    def __init__(self, client):
        self.client = client

        self.list_alarm_instance = ComponentAPI(
            client=self.client, method='POST',
            path='/api/c/compapi{bk_api_ver}/monitor_v3/get_shield/',
            description=u' 获取告警屏蔽'
        )