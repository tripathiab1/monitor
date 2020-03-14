# -*- coding: utf-8 -*-

import falcon
import logging

from app.log import log_setup

from app.api.common import base
from app.api.v1 import ssh_handle

log_setup("monitor", logging.INFO)
LOG = logging.getLogger("monitor")

class App(falcon.API):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        LOG.info('API Server is starting')

        self.add_route('/v1/ssh_attempts', ssh_handle.SSHAttempts())


middleware = []
application = App(middleware=middleware)

if __name__ == "__main__":
    from wsgiref import simple_server
    httpd = simple_server.make_server('0.0.0.0', 8085, application)
    httpd.serve_forever()
