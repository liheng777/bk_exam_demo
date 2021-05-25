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
import json

from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render

# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt
from blueking.component.shortcuts import get_client_by_request
from exam_application import models


def home(request):
    """
    首页
    """
    client = get_client_by_request(request)
    result = client.cc.search_business()
    biz_list = result.get('data').get('info')
    print(biz_list)
    return render(request, "exam_application/list.html", {'biz_list': biz_list})


def dev_guide(request):
    """
    开发指引
    """
    return render(request, "exam_application/operator_list.html")


def contact(request):
    """
    联系页
    """
    return render(request, "exam_application/echart.html")


def tree(request):
    return render(request, "exam_application/tree.html")


def get_sets(request):
    """
    根据业务查询集群
    @param request:
    @return:
    """
    client = get_client_by_request(request)
    bk_biz_id = request.GET.get('bk_biz_id', 2)
    _params = {
        'bk_biz_id': int(bk_biz_id)
    }
    result = client.cc.search_set(_params)
    return JsonResponse({'items': result.get('data').get('info')})


def get_biz_topo(request):
    """
    获取业务拓扑树
    """
    biz_id = request.GET.get('bk_biz_id', 2)
    result = get_client_by_request(request).cc.search_biz_inst_topo({'bk_biz_id': int(biz_id)})
    if result['result']:
        return JsonResponse({'result': True, 'data': get_topo_sub(result['data'])})
    else:
        return JsonResponse({'result': False, 'message': result['message']})


def get_topo_sub(data):
    res = []
    for child in data:
        obj = dict()
        obj['id'] = str(child['bk_inst_id']) + '_' + str(child['bk_obj_id'])
        obj['text'] = child['bk_inst_name']
        if child['child']:
            obj['children'] = get_topo_sub(child['child'])
        res.append(obj)
    return res


def get_hosts(request):
    bk_biz_id = request.GET.get('bk_biz_id', 8)
    bk_set_id = request.GET.get('bk_set_id')
    bk_module_id = request.GET.get('bk_module_id')
    client = get_client_by_request(request)
    result = client.cc.search_host(query_host_params(bk_biz_id, bk_set_id, bk_module_id))
    return JsonResponse({'result': True, 'data': result['data']['info']})


def query_host_params(bk_biz_id, bk_set_id, bk_module_id):
    _params = {
        "ip": {
            "data": [],
            "exact": 1,
            "flag": "bk_host_innerip|bk_host_outerip"
        },
        "condition": [],
        "page": {
            "start": 0,
            "limit": 10,
            "sort": "bk_host_id"
        },
        "pattern": ""
    }

    if bk_biz_id:
        bk_biz_id_params = {
            "bk_obj_id": "biz",
            "fields": [],
            "condition": [{
                "field": "bk_biz_id",
                "operator": "$eq",
                "value": int(bk_biz_id)
            }]
        }
        _params['condition'].append(bk_biz_id_params)

    if bk_set_id:
        bk_set_id_params = {
            "bk_obj_id": "set",
            "fields": [],
            "condition": [{
                "field": "bk_set_id",
                "operator": "$eq",
                "value": int(bk_set_id)
            }]
        }
        _params['condition'].append(bk_set_id_params)

    if bk_module_id and bk_module_id != 'None':
        bk_module_id_params = {
            "bk_obj_id": "module",
            "fields": [],
            "condition": [{
                "field": "bk_module_id",
                "operator": "$eq",
                "value": int(bk_module_id)
            }]
        }
        _params['condition'].append(bk_module_id_params)

    return _params


def do_execute_job(request):
    client = get_client_by_request(request)
    ip_list = [
        {
            'bk_cloud_id': 0,
            'ip': '10.1.2.9'
        }
    ]
    _params = {'bk_job_id': 1000, 'bk_biz_id': 2}
    bk_job_id = 1000
    bk_biz_name = request.GET.get('bk_biz_name', '蓝鲸')
    ip_list = json.loads(request.GET.get('ip_list')) if request.GET.get('ip_list') else ip_list
    job_detail_result = client.job.get_job_detail({'bk_job_id': 1000, 'bk_biz_id': 2})
    job_detail = job_detail_result.get('data')
    for step in job_detail.get('steps'):
        if step.get('ip_list'):
            step['ip_list'] = ip_list
    _params['steps'] = job_detail.get('steps')
    job_exec_result = client.job.execute_job(_params)
    job_instance_id = job_exec_result.get('data').get('job_instance_id')
    job_details = get_job_log(client, job_instance_id, bk_biz_id=2)
    go_save_history(request, job_details, bk_job_id, bk_biz_name)
    return JsonResponse({})


def get_job_log(client, job_instance_id, bk_biz_id):
    _params = {
        'bk_biz_id': bk_biz_id,
        'job_instance_id': job_instance_id,
    }
    result = client.job.get_job_instance_log(_params)
    while not result.get('data')[0].get('is_finished'):
        result = client.job.get_job_instance_log(_params)
    return result


def go_save_history(request, job_detail, bk_job_id, bk_biz_name):
    history = models.History()
    history.username = request.user.username
    history.bk_biz_name = bk_biz_name
    history.bk_job_id = bk_job_id
    history.status = job_detail.get('data')[0].get('status') if job_detail.get('data')[0].get('status') else 9
    ip_logs = job_detail['data'][0]['step_results'][0]['ip_logs']
    log = []
    ip_list = []
    for ip_log in ip_logs:
        log.append(ip_log.get('log_content'))
        ip_list.append(ip_log.get('ip'))
    history.ip_list = ';'.join(ip_list)
    history.log = ';'.join(log)
    history.save()


def get_chart(request):
    data = {'title': '', 'series': [], 'result': False}
    history_total_list = models.History.objects.values('status').annotate(value=Count('status'))
    data['series'] = list(history_total_list)
    for history in data['series']:
        history['name'] = status.get(str(history.get('status')))
    data['result'] = True
    return JsonResponse({'data': data})


status = {
    '1': '未执行',
    '2': '正在执行',
    '3': '执行成功',
    '4': '执行失败',
    '5': '跳过',
    '6': '忽略错误',
    '7': '等待用户',
    '8': '手动结束',
    '9': '状态异常',
    '10': '步骤强制终止中',
    '11': '步骤强制终止成功',
    '12': '步骤强制终止失败',

}