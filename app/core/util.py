import shutil
import logging
from logging import handlers
import colorlog
import os
import configparser
from inspect import currentframe
import time
import platform
import pymysql
import uuid
import requests
import hashlib
import chardet
import base64


class UniUtil:
    """统一处理工具类"""
    
    @staticmethod
    def base64_decrypt(base64_str: str) -> str:
        """使用base64模块解密字符串"""
        base64_bytes = base64_str.encode('utf-8')
        input_bytes = base64.b64decode(base64_bytes)
        return input_bytes.decode('utf-8')
    
    @staticmethod
    def base64_encrypt(input_str: str) -> str:
        """使用base64模块加密字符串"""
        input_bytes = input_str.encode('utf-8')
        base64_bytes = base64.b64encode(input_bytes)
        return base64_bytes.decode('utf-8')

    @staticmethod
    def get_file_md5(filepath: str):
        """获取文件的哈希值MD5"""
        m = hashlib.md5()
        with open(filepath, "rb") as fr:
            while True:
                # 将文件分块读取
                data = fr.read(1024)
                if not data:
                    break
                m.update(data)
        return m.hexdigest()

    @staticmethod
    def verify_url(url: str):
        """判断url是否可用"""
        res = False
        try:
            requests.packages.urllib3.disable_warnings()
            rep = requests.get(url, verify=False, timeout=10)
            if rep.status_code != 400:
                res = True
        except Exception as e:
            pass
        return res

    @staticmethod
    def uuids(param: str = None):
        """字典uuid"""
        if param is None:
            return uuid.uuid1()
        else:
            return str(uuid.uuid3(uuid.NAMESPACE_OID, str(param)))

    @staticmethod
    def get_uuid(param: dict = None):
        """基于名字的MD5散列值，同一命名空间的同一名字生成相同的uuid"""
        return UniUtil.uuids(param)

    @staticmethod
    def time_cost(fn):
        """这个装饰器用于统计函数运行耗时"""

        def _timer(*args, **kwargs):
            func_name = fn.__name__
            print('start', func_name)
            start = time.perf_counter()
            result = fn(*args, **kwargs)
            end = time.perf_counter()
            cost = _fmt(end - start)
            print('end', func_name)
            print('cost', cost)
            return result

        def _fmt(sec):
            """格式化打印时间，大于60秒打印分钟，大于60分钟打印小时"""
            return f'{round(sec, 2)}s' if sec <= 60 else f'{round(sec / 60, 2)}m' if sec <= 3600 else f'{round(sec / 3600, 2)}h'

        return _timer

    @staticmethod
    def range_partition(max, partitions=10, min=0):
        """根据数据范围划分区间
        :param min 最小值，默认值0
        :param max 最大值
        :param partitions 划分的区间数
        :return 返回划分后的区间集合 ['区间1', '区间2', '区间3', ...]
        """
        res = []
        interval = max / partitions
        while len(res) < partitions:
            start, end = min, min + interval
            res.append(f'{start:.1f} ~ {end:.1f}') if end < max else res.append(f'>= {min:.1f}')
            min += interval
        return res


    @staticmethod
    def del_none(li):
        """删除list中None"""
        return [e for e in li if e]

    @staticmethod
    def get_os():
        """获取当前操作系统"""
        return platform.system()

    @staticmethod
    def to_str(bytes_or_str):
        """
        把byte类型转换为str
        :param bytes_or_str:
        :return:
        """
        if isinstance(bytes_or_str, bytes):
            value = bytes_or_str.decode('utf-8')
        else:
            value = bytes_or_str
        return value


class ConfUtil:
    """配置文件【config.ini】操作工具类"""
    CONN = None
    CFID = None

    @classmethod
    def _init(cls, conf):
        cls.connect(conf)

    @classmethod
    def connect(cls, conf):
        cls.CONN = configparser.ConfigParser()
        cls.CONN.read(conf, encoding='utf-8')
        cls.CFID = UniUtil.uuids(conf)

    @classmethod
    def get_items(cls, conf, section):
        """获取某一章节的所有信息"""
        cls._init(conf)
        res = {}
        for item in cls.CONN.items(section):
            res[item[0]] = item[1]
        return res

    @classmethod
    def get_value(cls, conf, section, key):
        """根据章节id获取图片最终序号"""
        cls._init(conf)
        res = None
        if str(key) in cls.CONN.options(section):
            res = cls.CONN.get(section, str(key))
        return res

    @classmethod
    def set_value(cls, conf, section, key, value):
        """根据章节id设置图片最终序号"""
        cls._init(conf)
        cls.CONN.set(section, str(key), str(value))
        cls.CONN.write(open(conf, "w", encoding='utf-8'))


class FileUtil:
    """目录、文件操作工具类"""

    @staticmethod
    def mod_encoding(file: str, dst_encoding: str):
        """
        修改文件编码
        :param file:文件路径
        :dst_encoding:修改成什么编码
        """
        src_encoding = FileUtil.get_encoding(file)
        file_data = ""
        with open(file, "r", encoding=src_encoding) as f:
            for line in f:
                file_data += line
        with open(file, "w", encoding=dst_encoding) as f:
            f.write(file_data)

    @staticmethod
    def get_encoding(file: str):
        """
        获取文件编码
        :param file:文件路径
        :return:文件编码
        """
        with open(file, "rb") as fp:
            return chardet.detect(fp.read(1024 * 1024))["encoding"]

    @staticmethod
    def mod_file(file: str, lns: list, old_str: str, new_str: str):
        """替换文件指定的行的字符
        param file:文件名
        param lns:行号，指定的所有行都替换
        param old_str:旧字符串
        param new_str:新字符串
        """
        encoding = FileUtil.get_encoding(file)
        file_data, ln = "", 0
        with open(file, "r", encoding=encoding) as f:
            for line in f:
                ln += 1
                if ln in lns:
                    if old_str in line:
                        line = line.replace(old_str, new_str)
                file_data += line
        with open(file, "w", encoding=encoding) as f:
            f.write(file_data)

    @staticmethod
    def list_dir(filepath, contains: str = None):
        """列出目录下的所有文件
        :contains 包含的字符
        """
        res = []
        for file in os.listdir(filepath):
            fp = f'{filepath}/{file}'
            if contains:
                if contains in file:
                    res.append(fp)
            else:
                res.append(fp)
        res.sort()
        return res

    @staticmethod
    def create_dir_if_not_exist(dst_dir: str):
        """创建目录，不存在则创建，存在无操作
        :param dst_dir 要创建的目录
        """
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)

    @staticmethod
    def del_dir_or_file(dst_fd: str):
        """删除文件或目录
        :param src_fd 要删除的目录或文件
        """
        if os.path.isdir(dst_fd):
            shutil.rmtree(dst_fd)
        elif os.path.isfile(dst_fd):
            os.remove(dst_fd)

    @staticmethod
    def get_file_size(filepath: str):
        """获取文件或文件夹的大小
        注意：TB级别以及超过TB的数据就别用了，需要考虑性能了
        """
        res = 0
        # 判断输入是文件夹还是文件
        if os.path.isdir(filepath):
            # 如果是文件夹则统计文件夹下所有文件的大小
            for file in os.listdir(filepath):
                res += os.path.getsize(f'{filepath}/{file}')
        elif os.path.isfile(filepath):
            # 如果是文件则直接统计文件的大小
            res += os.path.getsize(filepath)
        # 格式化返回大小
        bu = 1024
        if res < bu:
            res = f'{bu}B'
        elif bu <= res < bu**2:
            res = f'{round(res / bu, 3)}KB'
        elif bu**2 <= res < bu**3:
            res = f'{round(res / bu**2, 3)}MB'
        elif bu**3 <= res < bu**4:
            res = f'{round(res / bu**3, 3)}GB'
        elif bu**4 <= res < bu**5:
            res = f'{round(res / bu**4, 3)}TB'
        return res

    @staticmethod
    def clear_dir(filepath: str):
        """清空文件夹下的所有文件，先删除文件夹再创建"""
        if not os.path.exists(filepath):
            os.mkdir(filepath)
        else:
            shutil.rmtree(filepath)
            os.mkdir(filepath)


class LogUtil:
    """日志工具类"""
    logger = None
    format = '%(asctime)s %(levelname)s: %(message)s'
    colors = {
        'DEBUG': 'cyan',
        'INFO': 'blue',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
    # 颜色格式
    fmt_colored, fmt_colorless = None, None
    # 日志输出端
    console_handler, file_handler = None, None

    @classmethod
    def init(cls, logname: str, console: bool = False):
        """使用前需要初始化，输入生成的日志文件名
        注意：默认按天生成日志，且保留最近一周的日志文件
        """
        if not cls.logger:
            pdir = '/'.join(logname.split('/')[:-1])
            if pdir:
                FileUtil.create_dir_if_not_exist(pdir)
            cls.logger = logging.getLogger(logname)
            cls.logger.setLevel(logging.DEBUG)
            # 有颜色格式
            cls.fmt_colored = colorlog.ColoredFormatter(f'%(log_color)s{cls.format}', datefmt=None, reset=True, log_colors=cls.colors)
            # 无颜色格式
            cls.fmt_colorless = logging.Formatter(cls.format)
            # 输出到控制台和文件
            if console:
                cls.console_handler = logging.StreamHandler()
            cls.file_handler = handlers.TimedRotatingFileHandler(filename=logname, when='D', backupCount=3, encoding='utf-8')

    @classmethod
    def open(cls):
        if cls.logger:
            if cls.console_handler:
                cls.console_handler.setFormatter(cls.fmt_colored)
                cls.logger.addHandler(cls.console_handler)
            if cls.file_handler:
                cls.file_handler.setFormatter(cls.fmt_colored)
                cls.logger.addHandler(cls.file_handler)
        else:
            print('Please init LogUtil first!')

    @classmethod
    def close(cls):
        if cls.console_handler:
            cls.logger.removeHandler(cls.console_handler)
        cls.logger.removeHandler(cls.file_handler)

    @classmethod
    def debug(cls, title: str = None, *msg):
        cls.open()
        lastframe = currentframe().f_back
        filepath = lastframe.f_code.co_filename
        funcn = lastframe.f_code.co_name
        lineo = lastframe.f_lineno
        cls.logger.debug("< {} >".format(title).center(100, "-"))
        cls.logger.debug(f'< {funcn} - {lineo} >')
        if msg or msg == 0 or msg is False:
            cls.logger.debug(msg)
        cls.logger.debug("")
        cls.close()

    @classmethod
    def info(cls, title: str = None, *msg):
        cls.open()
        lastframe = currentframe().f_back
        filepath = lastframe.f_code.co_filename
        funcn = lastframe.f_code.co_name
        lineo = lastframe.f_lineno
        if title:
            cls.logger.info("< {} >".format(title).center(100, "-"))
            cls.logger.info(f'< {funcn} - {lineo} >')
            if msg or msg == 0 or msg is False:
                cls.logger.info(msg)
        cls.logger.info("")
        cls.close()

    @classmethod
    def warn(cls, title: str = None, *msg):
        cls.open()
        lastframe = currentframe().f_back
        filepath = lastframe.f_code.co_filename
        funcn = lastframe.f_code.co_name
        lineo = lastframe.f_lineno
        if title:
            cls.logger.warn("< {} >".format(title).center(100, "-"))
            cls.logger.warn(f'< {funcn} - {lineo} >')
            if msg or msg == 0 or msg is False:
                cls.logger.warn(msg)
        cls.logger.warn("")
        cls.close()

    @classmethod
    def error(cls, title: str = None, *msg):
        cls.open()
        lastframe = currentframe().f_back
        filepath = lastframe.f_code.co_filename
        funcn = lastframe.f_code.co_name
        lineo = lastframe.f_lineno
        if title:
            cls.logger.error("< {} >".format(title).center(120, "#"))
            cls.logger.error(f'< {funcn} - {lineo} >')
            if msg or msg == 0 or msg is False:
                cls.logger.error(msg)
        cls.logger.error("")
        cls.close()

    @classmethod
    def critical(cls, title: str = None, *msg):
        cls.open()
        lastframe = currentframe().f_back
        filepath = lastframe.f_code.co_filename
        funcn = lastframe.f_code.co_name
        lineo = lastframe.f_lineno
        if title:
            cls.logger.critical("< {} >".format(title).center(120, "#"))
            cls.logger.critical(f'< {funcn} - {lineo} >')
            if msg or msg == 0 or msg is False:
                cls.logger.critical(msg)
        cls.logger.critical("")
        cls.close()


class MysqlUtil:
    """mysql工具类

    conf_mysql = {
        'host': '110.110.110.110',
        'port': 3306,
        'user': 'admin',
        'password': '123456',
        'database': 'db_test',
    }
    """
    CONN = None
    CFID = None

    @classmethod
    def _init(cls, conf: dict):
        cls.connect(conf)

    @classmethod
    def connect(cls, conf: dict):
        cls.CONN = pymysql.connect(**conf)
        cls.CFID = UniUtil.get_uuid(conf)

    @classmethod
    def get(cls, conf: dict, sql: str):
        cls._init(conf)
        res = None
        with cls.CONN.cursor() as cursor:
            cursor.execute(sql)
            res = cursor.fetchall()
        return res

    @classmethod
    def save(cls, conf: dict, sql: str):
        cls._init(conf)
        with cls.CONN.cursor() as cursor:
            cursor.execute(sql)
            cls.CONN.commit()
