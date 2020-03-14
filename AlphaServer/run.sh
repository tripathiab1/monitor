#!/usr/bin/env bash
export APP_ENV="live"

function start () {
    gunicorn -D -b 0.0.0.0:8085 --reload --timeout 300 \
             --log-file logs/monitor.log \
             --capture-output --log-level info app.main:application
}

function stop () {
    ps -ef | grep gunicorn | awk '{print $2}' | xargs kill -9
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    *)
    echo "Usage: run.sh {start|stop}"
    exit 1
esac

