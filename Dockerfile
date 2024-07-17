FROM python:3.7.8-alpine
WORKDIR /app
ADD . /app
RUN pip3 install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
CMD ["python3", "app/web_nav.py"]
