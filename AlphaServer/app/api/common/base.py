# -*- coding: utf-8 -*-

import falcon
import json
import logging

try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = dict

from app import log

LOG = logging.getLogger("monitor")

class BaseResource(object):

    def to_json(self, body_dict):
        return json.dumps(body_dict)

    def on_error(self, res, error=None):
        res.status = error['code']
        meta = OrderedDict()
        meta['code'] = error['code']
        meta['message'] = error['message']

        obj = OrderedDict()
        obj['meta'] = meta
        res.body = self.to_json(obj)

    def on_success(self, res, data=None):
        res.status = falcon.HTTP_200
        meta = OrderedDict()
        meta['code'] = 200
        meta['message'] = 'OK'

        obj = OrderedDict()
        obj['meta'] = meta
        obj['data'] = data
        res.body = self.to_json(obj)

