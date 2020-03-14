
import atexit
import os
import sys
import time
import logging
from signal import SIGTERM

logger = logging.getLogger("monitor")

def procexists(pid):
    """
    return true if process exists, false otherwise
    """

    try:
        os.kill(pid, 18)
    except OSError as v:
        return False

    return True

class Daemon(object):
	"""
	A generic daemon class.

	Usage: subclass the Daemon class and override the run() method
	"""

	def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null', chdir='/', pwd = None):
		self.stdin = stdin
		self.stdout = stdout
		self.stderr = stderr
		self.pidfile = pidfile
		self.chdir = chdir
		self.pwd = pwd

	def log(self, msg):
		logger.info("%s" % msg)

	def daemonize(self):
		"""
		do the UNIX double-fork magic, see Stevens' "Advanced
		Programming in the UNIX Environment" for details (ISBN 0201563177)
		http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
		"""
		try:
			pid = os.fork()
			if pid > 0:
				sys.exit(0)
		except OSError as e:
			sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
			sys.exit(1)

		os.chdir(self.chdir)
		os.setsid()
		os.umask(0)

		try:
			pid = os.fork()
			if pid > 0:
				sys.exit(0)
		except OSError as e:
			sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
			sys.exit(1)

		sys.stdout.flush()
		sys.stderr.flush()
		si = open(self.stdin, 'rb')
		so = open(self.stdout, 'ab+')
		se = open(self.stderr, 'ab+', 0)
		os.dup2(si.fileno(), sys.stdin.fileno())
		os.dup2(so.fileno(), sys.stdout.fileno())
		os.dup2(se.fileno(), sys.stderr.fileno())

		atexit.register(self.delpid)
		pid = str(os.getpid())
		open(self.pidfile,'w+').write("%s\n" % pid)

	def delpid(self):
		try:
			os.remove(self.pidfile)
		except OSError as e:
			return

	def start(self):
		if os.path.exists(self.pidfile):
			with open(self.pidfile, 'r') as pf:
				pid = int(pf.read().strip())
		else:
			pid = None

		if pid is not None:
			pexist = procexists(pid)
			if pexist:
				message = "pidfile %s already exist. Daemon already running?\n"
				logger.info(message % self.pidfile)
				return
			else:
				os.remove(self.pidfile)

		self.daemonize()
		self.run()

	def stop(self):
		try:
			with open(self.pidfile, 'r') as pf:
				pid = int(pf.read().strip())
		except IOError:
			pid = None

		if not pid:
			message = "pidfile %s does not exist. Daemon not running?\n"
			sys.stdout.write(message % self.pidfile)
			return

		try:
			while 1:
				os.kill(pid, SIGTERM)
				time.sleep(0.1)
		except OSError as err:
			err = str(err)
			if err.find("No such process") > 0:
				if os.path.exists(self.pidfile):
					os.remove(self.pidfile)
			else:
				print (str(err))
				sys.exit(1)

	def restart(self):
		"""
		Restart the daemon
		"""
		self.stop()
		self.start()

	def run(self):
		"""
		You should override this method when you subclass Daemon. It will be called after the process has been
		daemonized by start() or restart().
		"""
