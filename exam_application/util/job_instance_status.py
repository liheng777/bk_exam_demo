# -*- coding: utf-8 -*-
import time

from blueapps.utils.logger import logger
from config import SECRET_KEY, APP_CODE


def get_instance_status(client, username,  bk_biz_id, job_instance_id):
    instance_log_data = {
        "bk_app_code": APP_CODE,
        "bk_app_secret": SECRET_KEY,
        "bk_username": username,
        "bk_biz_id": bk_biz_id,
        "job_instance_id": job_instance_id,
    }
    logger.info('根据作业实例 ID 查询作业执行状态')
    job_info = client.job.get_job_instance_status(instance_log_data)
    while not job_info['data']["is_finished"]:
        time.sleep(5)
        job_info = client.job.get_job_instance_status(instance_log_data)
        if job_info['data']["is_finished"]:
            break
    return job_info['data']["is_finished"]
