# -*- coding: utf-8 -*-
from blueapps.utils.logger import logger
from config import APP_CODE, SECRET_KEY


def get_script_detail(client, username, script_id):
    """
    @param client:
    @param username:
    @param script_id:
    @return:
    """
    fast_execute_data = {
        "bk_app_code": APP_CODE,
        "bk_app_secret": SECRET_KEY,
        "bk_username": username,
        "account": "root",
        "bk_biz_id": 6,
        "id": script_id
    }
    # 执行脚本
    logger.info('根据脚本id查询脚本详情')
    info_script = client.job.get_script_detail(fast_execute_data)
    return info_script
