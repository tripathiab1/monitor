import platform
import os
import logging
import subprocess
import socket
import requests
from utils.endpoints import *
from config import PUSH_SERVER_URLS

logger = logging.getLogger("monitor")

# return sytem name like 'Linux', 'Darwin', 'Windows'
def get_system_name():

    return platform.system()

def get_host_name():

    return socket.gethostname()


class RESTfulOperation:
    """ REST related APIs """
    def post(self, url, body):
        """ RESTful POST call """
        resp = requests.post(url, json=body, verify=False)

        return resp


class SSHUtil:

    def __init__(self, system_name=None):
        self.system_name = system_name
        self.cmd_darwin_succ = 'cat /var/log/system.log | grep sshd | grep USER_PROCESS  | wc -l'
        self.cmd_darwin_failed = 'cat /var/log/system.log | grep com.openssh.sshd | wc -l'

    def successful_attempts(self):
        cmd = ''
        attempts = 0
        try:
            if self.system_name == 'Darwin':
                cmd = self.cmd_darwin_succ

            output = subprocess.check_output(cmd, shell=True)
            output = output.decode('utf-8').strip()
            attempts = int(output)
        except Exception as err:
            logger.error(err)

        return attempts

    def failed_attempts(self):
        cmd = ''
        attempts = 0
        try:
            if self.system_name == 'Darwin':
                cmd = self.cmd_darwin_failed

            output = subprocess.check_output(cmd, shell=True)
            output = output.decode('utf-8').strip()
            attempts = int(output)
        except Exception as err:
            logger.error(err)

        return attempts

    def get_ssh_attempts(self):

        succ_attempt = self.successful_attempts()
        failed_attempt = self.failed_attempts()

        return succ_attempt + failed_attempt

# utils for monitor client daemon 
class MonitorUtils(RESTfulOperation):

    def __init__(self):
        self.host_name = get_host_name()

    def monitor_windows(self):
        pass

    def monitor_linux(self):
        pass

    def monitor_darwin(self):
        try:
            ssh_attempts =  (SSHUtil('Darwin').get_ssh_attempts())
            logger.info('SSH Attempts: %s' % ssh_attempts)
            resp_data = {
                'host_name': self.host_name,
                'ssh_attempts': ssh_attempts
            }
            for server_url in PUSH_SERVER_URLS:
                 try:
                     url = SSH_ATTEMPTS_URL % server_url
                     resp = self.post(url, resp_data)
                     if resp.status_code != 200:
                         logger.error("Failed to push on %s" % server_url)
                         continue

                 except Exception as err:
                     logger.error(err)

        except Exception as err:
            logger.error(err)

    def run(self):
        system_name = get_system_name()

        if system_name == 'Darwin':
            self.monitor_darwin()
        elif system_name == 'Linux':
            self.monitor_linux()
        elif system_name == 'windows':
            self.monitor_windows()
