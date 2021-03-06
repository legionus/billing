#
# http.py
#
# Copyright (c) 2012-2013 by Alexey Gladkov
# Copyright (c) 2012-2013 by Nikolay Ivanov
#
# This file is covered by the GNU General Public License,
# which should be included with billing as the file COPYING.
#
__version__ = '1.0'

import json
import httplib

import secure
import message
import logging

LOG = logging.getLogger("jsonrpc.https")

class JsonRpcHttpError(Exception):
	def __init__(self, fmt, *args):
		Exception.__init__(self, fmt.format(*args))


def jsonrpc_http_request(pool, host, port, method, params=None, auth_data=None, req_limit=None):
	req = message.jsonrpc_request(method, params)
	LOG.debug(">>>Sending>>>:" + str(req))
	if auth_data:
		req = secure.jsonrpc_sign(auth_data['role'], auth_data['secret'], req)

	response = pool.request(host, port, "POST", "/", json.dumps(req))

	if response.status != httplib.OK:
		raise JsonRpcHttpError("The server returned an error: {0}.", response.reason)

		if req_limit:
			reply = response.read(req_limit + 1)

		if len(reply) > req_limit:
			raise JsonRpcHttpError("Got a reply of too big size.")
	else:
		reply = response.read()

	res = json.loads(reply)
	LOG.debug("<<<Reciving<<<:" + str(res))

	if not message.jsonrpc_is_response(res):
		raise JsonRpcHttpError("Got wrong response: {0}.", repr(res))

	if res['id'] != req['id']:
		raise JsonRpcHttpError("Got wrong reply id: {0}.", repr(res))

	return res
