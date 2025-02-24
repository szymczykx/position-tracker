#!/bin/bash

# 设置Python脚本的路径
SCRIPT_PATH="position_tracker.py"
PID_FILE="tracker.pid"
LOG_FILE="out.log"

start() {
    if [ -f "$PID_FILE" ] && ps -p $(cat "$PID_FILE") > /dev/null; then
        echo "程序已经在运行中"
        return
    fi
    
    echo "启动持仓监控程序..."
    nohup python3 "$SCRIPT_PATH" > "$LOG_FILE" 2>&1 & 
    echo $! > "$PID_FILE"
    echo "程序已启动，进程ID: $(cat "$PID_FILE")"
}

stop() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null; then
            echo "停止程序..."
            kill $PID
            rm "$PID_FILE"
            echo "程序已停止"
        else
            echo "程序未在运行"
            rm "$PID_FILE"
        fi
    else
        echo "找不到PID文件，程序可能未在运行"
    fi
}

status() {
    if [ -f "$PID_FILE" ] && ps -p $(cat "$PID_FILE") > /dev/null; then
        echo "程序正在运行，进程ID: $(cat "$PID_FILE")"
        echo "最近的日志:"
        tail -n 5 "$LOG_FILE"
    else
        echo "程序未在运行"
    fi
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    status)
        status
        ;;
    restart)
        stop
        sleep 1
        start
        ;;
    *)
        echo "使用方法: $0 {start|stop|status|restart}"
        exit 1
        ;;
esac

exit 0
