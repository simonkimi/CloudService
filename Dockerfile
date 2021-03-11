FROM python:3.9.2-slim

MAINTAINER simonkimi 805757448@qq.com

EXPOSE 8000
WORKDIR /var/service
RUN pip config set global.index-url https://pypi.doubanio.com/simple/
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
