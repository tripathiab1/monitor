import platform
import os
import logging

logger = logging.getLogger("monitor")

# return sytem name like 'Linux', 'Darwin', 'Windows'
def get_system_name():

    return platform.system()

class SSHUtil:

    def __init__(self, system_name=None):
        self.system_name = system_name

    def successful_attempts(self):
        attempts = 0

        return attempts

    def failed_attempts(self):
        attempts = 0

        return attempts

    def get_ssh_attempts(self):

        succ_attempt = self.successful_attempts()
        failed_attempt = self.failed_attempts()

        return succ_attempt + failed_attempt

# utils for monitor client daemon 
class MonitorUtils:

    def monitor_windows(self):
        pass

    def monitor_linux(self):
        pass

    def monitor_darwin(self):
        ssh_attempts =  (SSHUtil('Darwin').get_ssh_attempts())
        logger.info('SSH Attempts: %s' % ssh_attempts)
        pass

    def run(self):
        system_name = get_system_name()

        if system_name == 'Darwin':
            self.monitor_darwin()
        elif system_name == 'Linux':
            self.monitor_linux()
        elif system_name == 'windows':
            self.monitor_windows()
