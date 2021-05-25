# -*- coding: utf-8 -*-

import base64

from blueapps.utils.logger import logger
from config import APP_CODE, SECRET_KEY


def get_execute_script(client, username,  bk_biz_id, script_id, ip_list, script_param, script_content):
    fast_execute_data = {
        "bk_app_code": APP_CODE,
        "bk_app_secret": SECRET_KEY,
        "bk_username": username,
        "account": "root",
        "bk_biz_id": bk_biz_id,
        "ip_list": ip_list
    }
    if script_content:
        fast_execute_data['script_content'] = str(base64.b64encode(script_content.encode("utf-8")), "utf-8")
    if script_param:
        fast_execute_data['script_param'] = str(base64.b64encode(script_param.encode("utf-8")), "utf-8")
    if script_id:
        fast_execute_data['script_id'] = script_id
    logger.info('获取蓝鲸API中的fast_execute_script方法的作业实例')
    # 执行脚本
    info_script = client.job.fast_execute_script(fast_execute_data)
    #   作业实例ID
    job_instance_id = None
    if info_script.get("result"):
        #   获取作业实例ID
        job_instance_id = info_script.get("data").get("job_instance_id")
    return job_instance_id
