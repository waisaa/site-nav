# from core.const import Config
from core.util import MysqlUtil, LogUtil, ConfUtil
from core.const import *
import os

class Config:
    """数据库配置"""
    MYSQL = {
        'host': os.getenv('DB_HOST'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME'),
    }


def get_site_type():
    """获取网站类型"""
    res = {}
    sql = 'SELECT id, name FROM site_type'
    sql_res = MysqlUtil.get(Config.MYSQL, sql)
    for t in sql_res:
        res[t[1]] = t[0]
    # LogUtil.info('get_site_type', res)
    return res


def save_site(type, name, link):
    """保存网站地址"""
    sta, nm = 0, None
    sql_select = f"SELECT name FROM sites WHERE link = '{link}'"
    sql_insert = f"INSERT INTO sites(type_id, name, link) VALUES({type}, '{name}', '{link}')"
    res_select = MysqlUtil.get(Config.MYSQL, sql_select)
    if len(res_select) == 0:
        LogUtil.info('save_site', sql_insert)
        try:
            MysqlUtil.save(Config.MYSQL, sql_insert)
            sta = 1
        except Exception as e:
            LogUtil.error('site save failed', e)
    else:
        # LogUtil.warn('res_select', res_select[0][0])
        nm = res_select[0][0]
    return sta, nm


def get_site_by_name_like(name):
    """根据网站名称模糊查询"""
    res = {}
    sql = f"SELECT name, link FROM sites WHERE name LIKE '%{name}%'"
    LogUtil.info('sql', sql)
    sql_res = MysqlUtil.get(Config.MYSQL, sql)
    if sql_res:
        for t in sql_res:
            res[t[0]] = t[1]
    # LogUtil.info('get_site_by_name_like', res)
    return res


def get_sites_by_type(type):
    """根据类型获取网站"""
    res = {}
    sql = f'SELECT name, link FROM sites WHERE type_id = {type}'
    sql_res = MysqlUtil.get(Config.MYSQL, sql)
    if sql_res:
        for t in sql_res:
            res[t[0]] = f'{t[1]}\n'
    # LogUtil.info('get_sites_by_type', res)
    return res
