from pywebio import start_server, config
from pywebio.input import *
from pywebio.output import *
from pywebio.pin import *
from pywebio.session import *
from functools import partial
import random
from core.util import LogUtil, ConfUtil, FileUtil, UniUtil
import os
import time
from core.const import *
from db.crud import *
from core.func import *

LOG_FILE = os.path.split(__file__)[-1].split(".")[0]
LogUtil.init(f'logs/{LOG_FILE}.log')


def config_style():
    """自定义样式"""
    put_html(Style.CUSTOM)


def refresh():
    """刷新当前页面"""
    put_html(Style.REFRESH)


def get_bg_style():
    """获取背景样式"""
    bgimg = ConfUtil.get_value(Const.FILE_CONF, Const.SECTION_STYLE, Const.KEY_BGIMG)
    bgimgpath = f"static/imgs/bg/{bgimg}"
    bg_style = f"{Style.BG_PRE}{bgimgpath}{Style.BG_SUF}"
    # LogUtil.info("bg_style", bg_style)
    return bg_style


def edit_bg(choice, row):
    """编辑背景图片"""
    current_bg = ConfUtil.get_value(Const.FILE_CONF, Const.SECTION_STYLE, Const.KEY_BGIMG)
    if choice == Const.SET and current_bg != row:
        ConfUtil.set_value(Const.FILE_CONF, Const.SECTION_STYLE, Const.KEY_BGIMG, row)
        refresh()
        custom_config()
    elif choice == Const.DEL:
        img_file = f'{Const.DIR_BG}/{row}'
        FileUtil.del_dir_or_file(img_file)
        if current_bg != row:
            refresh()
        else:
            ConfUtil.set_value(Const.FILE_CONF, Const.SECTION_STYLE, Const.KEY_BGIMG, Const.IMG_BG_DEFAULT)
            refresh()
            custom_config()


def get_theme():
    """获取主题"""
    return ConfUtil.get_value(Const.FILE_CONF, Const.SECTION_STYLE, Const.KEY_THEME)


def write_record():
    config(title=Const.TITLE_WEB, theme=get_theme(), css_style=get_bg_style())
    config_style()
    back_home()
    put_html('''
        <div style="display: flex; align-items: left;">
            <img src="./static/imgs/edit.png" alt="edit" style="background-color: transparent;height:30px; margin-right: 10px; margin-top: 8px;">
            <span style="font-size: 30px;">信息录入</span>
        </div>
    ''')
    put_html('<hr style="border: 0.2px solid white;height:2px;">')
    write()


def write():
    """录入信息"""
    types = get_site_type()
    site_types = list(types.keys())
    LogUtil.info('types', site_types)
    put_select('site_type', label='网站类型', options=site_types).style('font-size: 120%')
    put_input('site_name', label='网站名称').style('font-size: 120%')
    put_input('site_link', label='网站地址', placeholder='Enter a valid url').style('font-size: 120%')
    btns = [dict(label='提交', value='ok', color='primary'), dict(label='重置', value='re', color='warning')]
    put_buttons(btns, small=False, group=True, outline=True, onclick=[do_save, refresh]).style('font-size: 120%')
    while True:
        pin_wait_change('site_type', 'site_name', 'site_link')
        site_type = pin.site_type
        site_name = pin.site_name
        site_link = pin.site_link
        LogUtil.info('site', site_type, site_name, site_link)
        local.site_type = types[site_type]
        if site_name:
            local.site_name = site_name
        if site_link and len(site_link) > 6:
            site_link = fmt_url(site_link)
            local.site_link = site_link
            if UniUtil.verify_url(site_link):
                local.site_valid = True
                toast('网站地址验证通过！', color='success')
            else:
                local.site_valid = True
                toast('网站地址无效！', color='error')


def do_save():
    """保存信息"""
    if local.site_name and local.site_valid:
        with popup('录入中...', closable=False, size=PopupSize.SMALL) as s:
            with put_loading(shape='grow', color='secondary').style('width:17rem; height:17rem'):
                UniUtil.download_favicon(local.site_link)
                sta, nm = save_site(local.site_type, local.site_name, local.site_link)
                close_popup()
                if sta == 1:
                    refresh()
                    toast('录入成功！', color='success')
                else:
                    toast(f'录入失败！【已收录：{nm}】', color='error')
    else:
        if not local.site_name:
            toast('网站名称未填！', color='error')
        elif not local.site_link:
            toast('网站地址未填！', color='error')
        elif local.site_valid is None:
            toast('网站地址验证中...', color='info')
        else:
            toast('网站地址无效！', color='error')


def search_for():
    config(title=Const.TITLE_WEB, theme=get_theme(), css_style=get_bg_style())
    config_style()
    back_home()
    put_html('''
        <div style="display: flex; align-items: left;">
            <img src="./static/imgs/search.png" alt="search" style="background-color: transparent;height:30px; margin-right: 10px; margin-top: 8px;">
            <span style="font-size: 30px;">信息搜索</span>
        </div>
    ''')
    put_html('<hr style="border: 0.2px solid white;height:2px;">')
    put_input('search', placeholder='请输入网站关键字').style('font-size: 130%')
    while True:
        changed = pin_wait_change('search', timeout=10)
        name_search = pin.search
        name_search = name_search if len(name_search) != 0 else None
        if name_search:
            name_search.replace("'", "")
        # LogUtil.info(f'name_search:{name_search}')
        res_search = get_site_by_name_like(name_search)
        with use_scope('res', clear=True):
            for k in res_search:
                web_site = res_search[k]
                favicon_path = UniUtil.download_favicon(web_site)
                put_html(f'<img src="{favicon_path}" alt="Image" style="background-color: transparent;height:18px;margin-right: 3px; margin-bottom: 3px;">')
                put_link(k, web_site, new_window=True).style('font-size: 130%')
                put_html('<div style="height: 10px;"></div>')


def get_link(name_link_dict):
    """获取连接地址"""
    res = []
    # LogUtil.info(f'name_link_dict:{name_link_dict}')
    for name in name_link_dict:
        web_site = name_link_dict[name]
        favicon_path = UniUtil.download_favicon(web_site)
        res.append(put_html(f'<img src="{favicon_path}" alt="Image" style="background-color: transparent;height:18px;margin-right: 3px; margin-bottom: 3px;">'))
        res.append(put_link(name, web_site, new_window=True).style('font-size: 20px;'))
        res.append(put_html('<div style="height: 10px;"></div>'))
    return res


def get_download_url(file: str):
    """业务函数"""
    hostip = ConfUtil.get_value(Const.FILE_CONF, Const.SECTION_DEPLOY, Const.KEY_HOSTIP)
    prefix = f'http://{hostip}:7777/static/downloads/'
    return f'{prefix}/{file}'


def downloads_tabs():
    """下载文件"""
    files = {}
    for file in os.listdir(Const.DIR_DOWLOAD):
        files[file] = get_download_url(file)
    links = get_link(files)
    return {'title': '下载', 'content': put_scrollable(links, height=380, keep_bottom=False, border=False)}


def get_tabs():
    """每种类型对应的所有网站
    元素：{'title': '网站类型', 'content': ['网站']}
    """
    res = []
    site_types = get_site_type()
    for type_name in site_types:
        sites = get_sites_by_type(site_types[type_name])
        links = get_link(sites)
        tab = {'title': type_name, 'content': put_scrollable(links, height=380, keep_bottom=False, border=False)}
        res.append(tab)
    # 下载文件
    # res.append(downloads_tabs())
    LogUtil.info(f'tabs:{res}')
    return res


def get_imgs():
    """获取背景图片"""
    res = []
    imgs = FileUtil.list_dir(Const.DIR_BG)
    for img in imgs:
        splits = img.split('/')
        img_file = splits[len(splits) - 1]
        disabled = True if img_file == Const.IMG_BG_DEFAULT else False
        btns = [dict(label='设置', value=Const.SET, color='primary'), dict(label='删除', value=Const.DEL, color='danger', disabled=disabled)]
        res.append([put_image(open(img, 'rb').read()), put_buttons(btns, small=True, group=True, outline=True, onclick=partial(edit_bg, row=img_file))])
    return res


def upload_img():
    img = file_upload(
        "选择图片:",
        accept="image/*",
        placeholder='选择一个图片',
        max_size='200M',
        multiple=False
    )
    if img:
        filename = f'bg{get_new_img_id()}.jpg'
        img_path = f'{Const.DIR_BG}/{filename}'
        content = img['content']
        with open(img_path, "wb") as output:
            output.write(content)
        toast('上传成功！', color='success')
        refresh()
        custom_config()
    else:
        toast('上传为空！', color='info')


def list_img():
    """背景图片列表"""
    put_scrollable(put_scope('bgimgs'), height=430, keep_bottom=False, border=False)
    put_table(get_imgs(), scope='bgimgs')


def change_theme():
    """改变主题"""
    current_theme = ConfUtil.get_value(Const.FILE_CONF, Const.SECTION_STYLE, Const.KEY_THEME)
    available_theme = [theme for theme in Const.THEMES if theme != current_theme]
    select_theme = available_theme[random.randint(0, 3)]
    ConfUtil.set_value(Const.FILE_CONF, Const.SECTION_STYLE, Const.KEY_THEME, select_theme)
    refresh()
    custom_config()


def back_home():
    """返回首页"""
    put_row([
        None,
        put_button("返回", onclick=lambda: go_app('index', new_window=False), color='danger', outline=True),
    ], size='92% 8%')


def show_loading():
    with popup('加载中...', closable=False, size=PopupSize.SMALL) as s:
        with put_loading(shape='grow', color='secondary').style('width:17rem; height:17rem'):
            # 使用 defer_call 来确保在 list_img 执行完后关闭弹窗
            defer_call(close_popup)


def custom_config():
    config(title=Const.TITLE_WEB, theme=get_theme(), css_style=get_bg_style())
    config_style()
    back_home()
    put_html('''
        <div style="display: flex; align-items: left;">
            <img src="./static/imgs/settings.png" alt="settings" style="background-color: transparent;height:30px; margin-right: 10px; margin-top: 8px;">
            <span style="font-size: 30px;">系统设置</span>
        </div>
    ''')
    put_html('<hr style="border: 0.2px solid white;height:2px;">')
    show_loading()
    list_img()
    close_popup()
    put_row([
        None,
        put_button("切换主题", onclick=lambda: change_theme(), color='success', outline=True),
        put_button("上传图片", onclick=lambda: upload_img(), color='success', outline=True),
        None,
    ], size='35% 15% 15% 35%')


def site_list():
    """管理列表"""
    config(title=Const.TITLE_WEB, theme=get_theme(), css_style=get_bg_style())
    config_style()
    back_home()
    put_markdown('# 管理').style('font-size: 25px')
    put_row([
        None,
        put_button("上一页", onclick=lambda: change_theme(), color='success', outline=True),
        put_button("上传图片", onclick=lambda: upload_img(), color='success', outline=True),
        put_button("下一页", onclick=lambda: upload_img(), color='success', outline=True),
        None,
    ], size='32% 12% 14% 12% 32%')


def index():
    config(title=Const.TITLE_WEB, theme=get_theme(), css_style=get_bg_style())
    config_style()
    put_row(
        [
            None,
            put_button("搜索", onclick=lambda: go_app('search_for', new_window=False), color='info', outline=True),
            put_button("录入", onclick=lambda: go_app('write_record', new_window=False), color='danger', outline=True),
            put_button("设置", onclick=lambda: go_app('custom_config', new_window=False), color='success', outline=True),
            # put_button("管理", onclick=lambda: go_app('site_list', new_window=False), color='success', outline=True),
        ],
        size='76% 8% 8% 8%')
    put_html('''
        <div style="display: flex; align-items: left;">
            <img src="./static/imgs/home.png" alt="home" style="background-color: transparent;height:30px; margin-right: 10px; margin-top: 8px;">
            <span style="font-size: 30px;">网站导航</span>
        </div>
    ''')
    put_html('<hr style="border: 0.2px solid white;height:2px;">')
    show_loading()
    tabs = get_tabs()
    close_popup()
    put_tabs(tabs).style('font-size: 130%;box-shadow: 0 15% 15% rgba(0, 0, 0, .2);')


def main():
    """网站导航"""
    LogUtil.info('')
    LogUtil.info('start success!')
    LogUtil.info('')
    start_server(
        applications=[
            index,
            write_record,
            search_for,
            custom_config,
            # site_list,
        ],
        # host='localhost',
        host='0.0.0.0',
        port=7777,
        debug=False,
        cdn=False,
        static_dir=Const.DIR_STATIC,
        # auto_open_webbrowser=True,
        # remote_access=True,
        reconnect_timeout=30,
        # allowed_origins=['*'],
    )


if __name__ == '__main__':
    main()
