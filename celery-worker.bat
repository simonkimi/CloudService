@echo off
title celery worker
celery -A asynchronous worker --loglevel=info -P eventlet