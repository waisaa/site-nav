# 使用 Python 基础镜像
FROM python:3.7.8-alpine

# 设置工作目录
WORKDIR /wkd

# 添加当前目录下所有文件到镜像中的 /wkd 目录
ADD . /wkd

# 安装 Python 依赖
RUN pip3 install --no-index --find-links=/wkd/pip3-libs/ -r /wkd/requirements.txt

# 暴露 Web 服务端口
EXPOSE 7777

# 启动 Python 服务
CMD ["python3", "/wkd/app/web_nav.py"]
