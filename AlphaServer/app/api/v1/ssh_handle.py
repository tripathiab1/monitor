# -*- coding: utf-8 -*-

import re
import falcon
import logging

from app import log
from app.api.common import BaseResource
import json

LOG = logging.getLogger("monitor")

class SSHAttempts(BaseResource):
    """
    Handle for endpoint: /v1/ssh_attempts
    """
    def on_post(self, req, res):
        """ API to push ssh attempts """
        resp = {}
        try:
            req_data = req.stream.read(req.content_length or 0).decode('utf-8')
            resp = {"resp": req_data}
            LOG.info(resp)
        except Exception as err:
            resp = {
                     "message": {
                                  "error": err,
                                },
                     "status": 0,
                     "code": falcon.HTTP_500
                   }
            LOG.error(resp)
            self.on_error(res, json.dumps(resp))

        self.on_success(res, json.dumps(resp))

