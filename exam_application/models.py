# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2020 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

# from django.db import models

# Create your models here.
from datetime import datetime

from django.db import models


class History(models.Model):
    username = models.CharField(max_length=32, verbose_name=u'用户名')
    bk_biz_name = models.CharField(max_length=64, verbose_name=u'业务名称', null=True)
    bk_job_id = models.IntegerField(verbose_name=u'作业ID', null=True)
    ip_list = models.TextField(verbose_name=u'主机列表', null=True)
    result = models.IntegerField(verbose_name=u'作业执行结果', null=True)
    log = models.TextField(verbose_name=u'作业执行日志', null=True)
    status = models.IntegerField(verbose_name=u'作业执行状态', null=True)
    created = models.DateField(verbose_name=u'创建时间', default=datetime.now)

    class Meta:
        db_table = 'history'
        verbose_name = u'执行历史'
        verbose_name_plural = verbose_name
