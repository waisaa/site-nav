<div align="center">

# WebNav

*网站导航*

[![](https://img.shields.io/badge/webui-webnav-9cf.svg)](http://192.168.18.13:7777/) [![](https://img.shields.io/badge/document-pywebio-blue.svg)](https://pywebio.readthedocs.io/) [![](https://img.shields.io/badge/license-WLF-brightgreen.svg)](https://gitlab.cloudansys.cn:8443/dep-deve-server/pms/web-nav/-/blob/master/LICENSE)

</div>

基于python轻量级框架PyWebIO开发的网站导航。支持网站分类展示、全局模糊查询及主题壁纸设置等功能。

## 页面截图

![](./resources/imgs/webnav.png)


## 看板娘配置 waifu.css
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6/css/all.min.css">
<script src="https://cdn.jsdelivr.net/gh/stevenjoezhang/live2d-widget@latest/autoload.js"></script>
```
 
## 背景图片设置
```html
<style>
body {
    overflow: hidden;
    position: fixed;
    width:100%;
    height:100%;
    background: url("http://elephant:7777/imgs/bg.jpg") no-repeat;
    background-size:cover;
}
</style>
```