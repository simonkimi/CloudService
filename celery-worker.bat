@echo off
title celery worker
celery -A asynchronous worker --loglevel=info --pool=solo -c 50