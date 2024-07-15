#!/bin/bash  

:<<!
【脚本说明】
1、此脚本适用操作python程序；
2、支持服务启动、停止、重启、查看状态、查看日志；
!

# 程序名称
app=web_nav
# 启动命令
run_cmd="python3 app/$app.py"

# 服务基本信息
operate=$1
ps_1=$app.py
dir_home=$(cd $(dirname $0);pwd)
log_file=$dir_home/logs/$app.log
pid_1=`ps -ef | grep $ps_1 | grep -v grep | awk '{print $2}'`

# 提示信息
msg="Please input the param 【<run|kil|res|sta|log>】"

# 定制化shell输出
function custom_print(){
    echo -e "\033[5;34m ***** \033[0m"
    echo -e "\033[32m $@ ! \033[0m"
    echo -e "\033[5;34m ***** \033[0m"
}

# 启动命令
function run(){
    nohup $run_cmd > /dev/null 2>&1 &
}

# 启动服务
if [[ $operate = "run" || $operate = "start" ]]; then
    if [[ ! $pid_1 ]]; then
        run
        msg='Start success'
        custom_print $msg
    else
        msg='The service is already running'
        custom_print $msg
    fi

# 停止服务
elif [[ $operate = "kil" || $operate = "stop" ]]; then
    if [[ $pid_1 ]]; then
        kill -9 $pid_1
        msg='Stopped success'
        custom_print $msg
    else
        # 服务早已停止或未启动
        msg='The service is already down'
        custom_print $msg
    fi

# 重启服务
elif [[ $operate = "res" || $operate = "restart" ]]; then
    if [[ $pid_1 ]]; then
        kill -9 $pid_1
    fi
    run
    msg='Restart success'
    custom_print $msg

# 查看服务运行状态
elif [[ $operate = "sta" || $operate = "status" ]]; then
    if [[ $pid_1 ]]; then
        # 黄底蓝字
        echo -e "\033[43;34m RUNNING \033[0m"
    else
        # 蓝底黑字
        echo -e "\033[44;30m STOPPED \033[0m"
    fi

# 查看服务运行日志
elif [[ $operate = "log" ]]; then
    if [[ -e $log_file ]]; then
        tail -f $log_file
    else
        msg="No logs have been generated so far"
        custom_print $msg
    fi

else
    custom_print $msg
fi
