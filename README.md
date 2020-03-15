VM Monitor
===

VM Monitor is a agent base tool based on client-server paradigm to monitor any Linux,  
Windows and Mac machine. This tool is written in Python 3+.

This tool has two main components:  
```
1. AlphaServer
2. AlphaClient
```

# Supported Features

```
1. Client push all ssh attempts to server and server keeps the message in log file
```

## Supported OS

```
1. Mac os
2. Linux (next release)
3. Windows (next release)
```

## AlphaServer

AlphaServer is falcon based application server which has APIs expose to push data from client.
Server will be run through `gunicorn` is a gateway interface HTTP server.
It is designed in a such way that next feature will be easily integrated.

## Directory Structure
```
.
├── app
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── common
│   │   │   ├── __init__.py
│   │   │   └── base.py
│   │   └── v1
│   │       ├── __init__.py
│   │       └── ssh_handle.py
│   ├── config.py
│   ├── log.py
│   └── main.py
├── conf
│   └── live.ini
├── logs
├── requirements.txt
└── run.sh
```

## Setup and run AlphaServer

```
$ git clone git@github.com:codeArrow/vm-monitor.git
$ cd vm-monitor/AlphaServer
$ virtualenv -p python3 .venv
$ source .venv/bin/activate
$ pip3 install -r requirements.txt

Then for interactive run:

$ gunicorn -b 0.0.0.0:8085 --reload --timeout 300 \
             --log-file logs/monitor.log \
             --capture-output --log-level info app.main:application

else run the following script:

$ bash run.sh start (to start service)
or
$ bash run.sh stop (to stop service)

```

Now you can monoitor log:

```
$ tail -f logs/monitor.log
```

## Future feature
Will keep all data in mysql database instead of keeping in logs or console


## AlphaClient

AlphaClient is a client deamon which will be deployed on the hosts needs to be monitor.  
Its a long lived process running host machine, and also could be added to cron server for wake up,   
if it is dead somehow. AlphaClient should be configure to multiple AlphaServers.  
It is responsible to collect and push data to configured AlphaServers.


## Directory Structre

```
.
├── config.py
├── daemon.py
├── log_config.py
├── logs
├── requirements.txt
├── settings.py
├── supervisord.py
├── tmp
└── utils
    ├── __init__.py
    ├── endpoints.py
    └── util.py

```


## Setup and run AlphaClient

```
$ git clone git@github.com:codeArrow/vm-monitor.git
$ cd vm-monitor/AlphaServer
$ virtualenv -p python3 .venv
$ source .venv/bin/activate
$ pip3 install -r requirements.txt
$ python3 supervisord.py start
or
$ python3 supervisord.py stop
```

Now you can monoitor log:

```
$ tail -f logs/monitor.logs
```

## Future feature
Will add monitoring for Linux and Windows OS as well
