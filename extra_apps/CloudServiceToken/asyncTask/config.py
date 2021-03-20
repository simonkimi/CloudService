from celery.schedules import crontab

host = "redis"
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
imports = ('asyncTask.tasks',)

TASK_SERIALIZER = 'pickle'
