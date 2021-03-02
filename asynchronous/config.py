from celery.schedules import crontab
host = "127.0.0.1"
port = "6379"
password = "123456"

broker_url = f'redis://{host}:{port}/0'
# 配置结果后端
result_backend = f'redis://{host}:{port}/1'
# 配置时区
enable_utc = False
timezone = 'Asia/Shanghai'
# 限制时间
CELERY_TASK_SOFT_TIME_LIMIT = CELERY_TASK_TIME_LIMIT = 10 * 60
# 配置需要导入的任务模块
imports = ('asynchronous.tasks', )

TASK_SERIALIZER = 'pickle'
beat_schedule = {
    'schedule-test': {
        'task': 'asynchronous.tasks.find_need_operate_user',  # 定时执行的任务的函数名称
        'schedule': crontab(minute="*/1")  # 定时执行的间隔时间
    }
}
