VM Monitor
===

VM Monitor is a agent base tool based on client-server paradigm to monitor any Linux,  
Windows and Mac machine. This tool is written in Python 3+.

This tool has two main components:  
```
1. AlphaServer
2. AlphaClient
```

## Supported Features

```
1. Client push all ssh attempts (successful and failed both) to server and server keeps the message in log file
```


## Supported OS

```
1. Mac os
2. Linux: ubuntu and (others will be next release) 
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
$ cd vm-monitor/AlphaClient
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

## Configure AlphaClient with AlphaServer
TODO

## Output
Output in the server log file will be look like:

```
{
	"host_name": "Ashtas-Mac-Pro.local",
	"ssh_attempts": {
		"ssh_succ_attempts": 0,
		"ssh_failed_attempts": 0
	},
	"machine_info": {
		"cpu_count": 2,
		"disk_partitions": [
			["/dev/disk1s1", "/", "apfs", "rw,local,rootfs,dovolfs,journaled,multilabel"],
			["/dev/disk1s4", "/private/var/vm", "apfs", "rw,noexec,local,dovolfs,dontbrowse,journaled,multilabel,noatime"],
			["/Users/ashta/Downloads/Visual Studio Code.app", "/private/var/folders/b6/kb0x7nrj5n35s0gv8jzkt9040000gp/T/AppTranslocation/BA1837EB-6AE0-4EB7-9A7E-F229E6B4D5A1", "nullfs", "ro,nosuid,local,dontbrowse,multilabel"]
		],
		"disk_io_counters": [{
			"disk0": {
				"read_count": 3666829,
				"write_count": 3606644,
				"read_bytes": 65363664896,
				"write_bytes": 53277241344,
				"read_time": 2020240,
				"write_time": 1202666
			}
		}],
		"net_io_counters": {
			"bytes_sent": 500190208,
			"bytes_recv": 5563761664,
			"packets_sent": 3339372,
			"packets_recv": 5731933,
			"errin": 0,
			"errout": 0,
			"dropin": 0,
			"dropout": 0
		},
		"net_connections": {
			"48819": {
				"info": {
					"ip": "0.0.0.0",
					"port": 138
				},
				"status": "NONE"
			},
			"48816": {
				"info": {
					"ip": "0.0.0.0",
					"port": 8085
				},
				"status": "LISTEN"
			},
			"44053": {
				"info": {
					"ip": "0.0.0.0",
					"port": 8085
				},
				"status": "LISTEN"
			},
			"19768": {
				"info": {
					"ip": "192.168.5.178",
					"port": 49951
				},
				"status": "ESTABLISHED"
			},
			"19766": {
				"info": {
					"ip": "192.168.5.178",
					"port": 50883
				},
				"status": "ESTABLISHED"
			},
			"19762": {
				"info": {
					"ip": "0.0.0.0",
					"port": 0
				},
				"status": "NONE"
			},
			"43897": {
				"info": {
					"ip": "0.0.0.0",
					"port": 0
				},
				"status": "NONE"
			},
			"1166": {
				"info": {
					"ip": "127.0.0.1",
					"port": 15292
				},
				"status": "LISTEN"
			},
			"1119": {
				"info": {
					"ip": "0.0.0.0",
					"port": 56976
				},
				"status": "NONE"
			},
			"1117": {
				"info": {
					"ip": "127.0.0.1",
					"port": 49298
				},
				"status": "LISTEN"
			},
			"977": {
				"info": {
					"ip": "::",
					"port": 33060
				},
				"status": "LISTEN"
			},
			"806": {
				"info": {
					"ip": "::1",
					"port": 6379
				},
				"status": "LISTEN"
			},
			"791": {
				"info": {
					"ip": "0.0.0.0",
					"port": 0
				},
				"status": "NONE"
			},
			"769": {
				"info": {
					"ip": "192.168.5.178",
					"port": 50900
				},
				"status": "ESTABLISHED"
			},
			"738": {
				"info": {
					"ip": "192.168.5.178",
					"port": 53818
				},
				"status": "NONE"
			},
			"717": {
				"info": {
					"ip": "0.0.0.0",
					"port": 0
				},
				"status": "NONE"
			},
			"676": {
				"info": {
					"ip": "0.0.0.0",
					"port": 0
				},
				"status": "NONE"
			},
			"672": {
				"info": {
					"ip": "0.0.0.0",
					"port": 0
				},
				"status": "NONE"
			},
			"669": {
				"info": {
					"ip": "0.0.0.0",
					"port": 0
				},
				"status": "NONE"
			},
			"654": {
				"info": {
					"ip": "0.0.0.0",
					"port": 0
				},
				"status": "NONE"
			},
			"592": {
				"info": {
					"ip": "192.168.5.178",
					"port": 49941
				},
				"status": "ESTABLISHED"
			},
			"296": {
				"info": {
					"ip": "0.0.0.0",
					"port": 0
				},
				"status": "NONE"
			},
			"263": {
				"info": {
					"ip": "0.0.0.0",
					"port": 0
				},
				"status": "CLOSE"
			},
			"172": {
				"info": {
					"ip": "0.0.0.0",
					"port": 0
				},
				"status": "NONE"
			},
			"160": {
				"info": {
					"ip": "::",
					"port": 57042
				},
				"status": "NONE"
			},
			"133": {
				"info": {
					"ip": "0.0.0.0",
					"port": 0
				},
				"status": "NONE"
			},
			"104": {
				"info": {
					"ip": "0.0.0.0",
					"port": 0
				},
				"status": "NONE"
			},
			"100": {
				"info": {
					"ip": "0.0.0.0",
					"port": 0
				},
				"status": "NONE"
			},
			"95": {
				"info": {
					"ip": "0.0.0.0",
					"port": 0
				},
				"status": "NONE"
			},
			"86": {
				"info": {
					"ip": "0.0.0.0",
					"port": 0
				},
				"status": "NONE"
			},
			"78": {
				"info": {
					"ip": "0.0.0.0",
					"port": 0
				},
				"status": "CLOSE"
			},
			"53": {
				"info": {
					"ip": "0.0.0.0",
					"port": 0
				},
				"status": "NONE"
			},
			"51": {
				"info": {
					"ip": "0.0.0.0",
					"port": 0
				},
				"status": "NONE"
			},
			"1": {
				"info": {
					"ip": "0.0.0.0",
					"port": 137
				},
				"status": "NONE"
			}
		},
		"net_if_addrs": [{
			"lo0": "127.0.0.1"
		}, {
			"en0": "192.168.5.178"
		}],
		"battery": {
			"percent": 50,
			"secsleft": 13380,
			"power_plugged": false
		},
		"users": [{
			"name": "ashta",
			"terminal": "console",
			"host": null,
			"started": 1587622400.0,
			"pid": 95
		}, {
			"name": "ashta",
			"terminal": "ttys002",
			"host": null,
			"started": 1587623552.0,
			"pid": 3196
		}, {
			"name": "ashta",
			"terminal": "ttys003",
			"host": null,
			"started": 1587623552.0,
			"pid": 3206
		}, {
			"name": "ashta",
			"terminal": "ttys004",
			"host": null,
			"started": 1587623552.0,
			"pid": 3216
		}, {
			"name": "ashta",
			"terminal": "ttys005",
			"host": null,
			"started": 1587623552.0,
			"pid": 3226
		}, {
			"name": "ashta",
			"terminal": "ttys006",
			"host": null,
			"started": 1587623552.0,
			"pid": 3236
		}, {
			"name": "ashta",
			"terminal": "ttys007",
			"host": null,
			"started": 1587623552.0,
			"pid": 3246
		}, {
			"name": "ashta",
			"terminal": "ttys008",
			"host": null,
			"started": 1587623552.0,
			"pid": 3256
		}, {
			"name": "ashta",
			"terminal": "ttys009",
			"host": null,
			"started": 1587623552.0,
			"pid": 3260
		}, {
			"name": "ashta",
			"terminal": "ttys010",
			"host": null,
			"started": 1587724544.0,
			"pid": 6650
		}, {
			"name": "ashta",
			"terminal": "ttys011",
			"host": null,
			"started": 1587927424.0,
			"pid": 43933
		}, {
			"name": "ashta",
			"terminal": "ttys012",
			"host": null,
			"started": 1587959424.0,
			"pid": 53679
		}]
	}
}
```


## Future feature
Will add monitoring for Windows OS as well
