import datetime
import django_celery_beat

import django
from celery.task import task
from django.utils import timezone
from blueapps.utils.logger import logger
from blueking.component.shortcuts import get_client_by_user

from celery.task import periodic_task
from django.utils import timezone
from django_celery_beat.tzcrontab import TzAwareCrontab


def execute_task(username, dict_param, on_line_data):
    """
    username: 当前登录用户
    template_id: 模板id
    dict_param: 修改上线状态相关数据
    on_line_data: 上线工程相关信息
    package_type: 1前端，2后端

    执行 celery 异步任务

    调用celery任务方法:
        task.delay(arg1, arg2, kwarg1='x', kwarg2='y')
        task.apply_async(args=[arg1, arg2], kwargs={'kwarg1': 'x', 'kwarg2': 'y'})
        delay(): 简便方法，类似调用普通函数
        apply_async(): 设置celery的额外执行选项时必须使用该方法，如定时（eta）等
                      详见 ：http://celery.readthedocs.org/en/latest/userguide/calling.html
    """
    now = datetime.datetime.now()
    logger.error(u"celery 异步任务，将在5s后执行，当前时间：{}".format(now))
    # we_work = WeWorkAppInfo()
    # we_work.agentid = APPID
    # we_work.corp_id = SCORPID
    # we_work.secret = CORPSECRET
    # we_work.access_token = STOKEN
    # we_work.save()
    # 调用定时任务
    start_task.apply_async(args=[username, dict_param, on_line_data],
                           eta=django.utils.timezone.now() + datetime.timedelta(seconds=5))


@task()
def start_task(username, dict_param, on_line_data):
    """
    定义一个 celery 异步任务
    """
    client = get_client_by_user(username)
    pass


@periodic_task(
    run_every=django_celery_beat.tzcrontab.TzAwareCrontab(minute='*', hour='*', day_of_week="*", day_of_month='*',
                                                          month_of_year='*', tz=timezone.get_current_timezone()))
def timing_del_test_log():
    """
    定时任务
    """
    logger.info("时间：{datetime}".format(datetime=str(datetime.datetime.now())))

    return True
