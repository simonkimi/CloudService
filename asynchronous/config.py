import os
from celery.schedules import crontab
from kombu import Exchange, Queue

host = "redis" if os.getenv('DOCKER', '0') == '1' else '127.0.0.1'
port = "6379"

broker_url = f'redis://{host}:{port}/0'
# 配置结果后端
result_backend = f'redis://{host}:{port}/1'
# 配置时区
enable_utc = False
timezone = 'Asia/Shanghai'
# 限制时间
CELERY_TASK_SOFT_TIME_LIMIT = CELERY_TASK_TIME_LIMIT = 10 * 60
# 配置需要导入的任务模块
imports = ('asynchronous.tasks', 'asynchronous.login_task')

TASK_SERIALIZER = 'pickle'
beat_schedule = {
    'schedule-test': {
        'task': 'asynchronous.tasks.find_need_operate_user',  # 定时执行的任务的函数名称
        'schedule': crontab(minute="*/1")  # 定时执行的间隔时间
    }
}

task_queues = (
    Queue('token', Exchange('token', type='direct'), routing_key='token'),
    Queue('game', Exchange('game', type='direct'), routing_key='game'),
)

task_routes = (
    {'asynchronous.login_task.get_token': {
        'queue': 'token',
        'routing_key': 'token'
    }},
    {'asynchronous.tasks.execute': {
        'queue': 'game',
        'routing_key': 'game'
    }},
    {'asynchronous.tasks.find_need_operate_user': {
        'queue': 'game',
        'routing_key': 'game'
    }}
)
