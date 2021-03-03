@echo off
title celery beat
celery -A asynchronous beat
pause