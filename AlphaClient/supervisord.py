#!/usr/bin/python

import datetime
import gc
import os
import subprocess
import sys
import time
import threading
import settings
from daemon import Daemon
from log_config import *
from utils.util import MonitorUtils

sys.path = ["../"] + sys.path

MAIN_SLEEP = 10 # seconds
TMPDIR = 'logs/'

log_setup("monitor", MAIN_THREAD_LOG_FILE, logging.INFO)
logger = logging.getLogger("monitor")

#
# workaround to disable InsecurePlatformWarning 
# warning for SSL during login. From python 2.7.9+
# security packages were a part of request module
#
try:
    import requests.packages.urllib3
    requests.packages.urllib3.disable_warnings()
except:
    # not a part of request package from python 2.7.9+
    pass

__cmdpy = "supervisord"

def usage():
    print ("\n\t - To start %s - 'python3 %s start'" % (__cmdpy, __cmdpy))
    print ("\t - To stop %s - 'python3 %s stop'" % (__cmdpy, __cmdpy))
    print ("\t - To restart %s - 'python3 %s restart'" % (__cmdpy, __cmdpy))



class Supervisor(Daemon):


    def monitor(self, **kwargs):
        """
        Periodically monitor machine
        """
        obj = MonitorUtils()
        while True:
            try:
                with settings.lock:
                    obj.run()
                if settings.stop:
                    return
            except Exception as err:
                logger.exception(err)

            gc.collect()
            time.sleep(MAIN_SLEEP)

        return


    def run(self):
        """ Running the daemon excution code """
        logger.info('Started monitoring')
        settings.init()

        while True:
            logger.info("Starting monitoring threads.")
            m = threading.Thread(target = self.monitor, kwargs={})
            m.start()
            settings.nthreads += 1
            break

if __name__ == '__main__':
    if len(sys.argv) == 1:
        cmd = 'start'
    else:
        cmd = sys.argv[1]

    if cmd not in ("start", "stop", "restart"):
        usage()
        sys.exit(2)

    PIDFILE = "tmp/monitor.pid"

    __supervisor = Supervisor(
        pidfile=PIDFILE,
        chdir=os.getcwd()
        )

    if 'start' == cmd:
        settings.stop = False
        __supervisor.start()
    elif 'stop' == cmd:
        settings.stop = True
        __supervisor.stop()
    elif 'restart' == cmd:
        settings.stop = False
        __supervisor.restart()
    else:
        print ("Unknown command")
        sys.exit(2)

    sys.exit(0)
