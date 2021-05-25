# -*- coding: utf-8 -*-
import time

from blueapps.utils.logger import logger
from config import SECRET_KEY, APP_CODE


def get_task_status(client, username, task_id):
    """
    :param client: 执行蓝鲸api
    :param username: 用户名
    :param task_id: 任务id
    :return:
    """
    task_data = {
        "bk_app_code": APP_CODE,
        "bk_app_secret": SECRET_KEY,
        "bk_username": username,
        'bk_biz_id': 6,
        "task_id": task_id
    }
    logger.info('查询任务或任务节点执行状态')
    err_flag = 0
    task_info = client.sops.get_task_status(task_data)
    while not task_info['result'] and err_flag < 3:
        time.sleep(5)
        task_info = client.sops.get_task_status(task_data)
        if task_info['result']:
            break
        err_flag += 1
    flag = 0
    while task_info['result'] and task_info['data']['state'] == 'RUNNING' and flag < 60:
        time.sleep(5)
        task_info = client.sops.get_task_status(task_data)
        if task_info['result'] and task_info['data']['state'] != 'RUNNING':
            break
        flag += 1
    logger.info('返回执行结果=>' + str(task_info))
    return task_info
