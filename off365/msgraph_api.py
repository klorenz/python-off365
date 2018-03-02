AUTHORITY = "https://login.microsoftonline.com"
RESOURCE = "https://graph.microsoft.com"

import requests
import adal
import sys
import time
import pprint
import logging
logger = logging.getLogger('off365.msgraph_api')

from urllib import urlencode
from .util import f


class MSGraphApi:
    def __init__(self, client_id, tenant, client_secret=None, username=None, password=None, state=None, resource=RESOURCE, **opts):
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.tenant = tenant
        self.state = state
        self.token = None
        self.expiresAt = 0
        self.resource = resource

    # service plan reference: https://docs.microsoft.com/de-de/azure/active-directory/active-directory-licensing-product-and-service-plan-reference

    def check_token(self):
        if self.expiresAt < time.time():
            authority = f("{AUTHORITY}/{tenant}")
            context = adal.AuthenticationContext(authority)
            self.token = context.acquire_token_with_username_password(
                self.resource, self.username, self.password, self.client_id)
            self.accessToken = self.token['accessToken']
            self.expiresAt = time.time() + self.token['expiresIn']

    def headers(self):
        self.check_token()
        headers = {
            'User-Agent': 'python_off365/1.0',
            'Authorization': f('Bearer {accessToken}'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        return headers

    def getUserPrincipalName(self, name):
        if "@" not in name:
            return f("{name}@{tenant}")
        else:
            return name

    def get(self, endpoint, params=None, headers={}, **parameter):
        if endpoint.startswith('https://'):
            url = endpoint
        elif endpoint.startswith('/'):
            url = f("https://graph.microsoft.com{endpoint}")
        else:
            url = f("https://graph.microsoft.com/v1.0/{endpoint}")

        print("url: %s" % url)
        pprint.pprint(params)

        _params = {}
        if params is not None:
            _params.update(params)
        _params.update(parameter)

        if '?' in url:
            url += "&" + urlencode(_params)
        else:
            url += "?" + urlencode(_params)

        _headers = self.headers()
        _headers.update(headers)

        url = url.replace("%2C", ',')

        return requests.get(url, headers=_headers)

    def patch(self, endpoint, params, headers={}, **parameter):
        return self.json_request('patch', endpoint, params, headers, **parameter)

    def post(self, endpoint, params, headers={}, **parameter):
        return self.json_request('post', endpoint, params, headers, **parameter)

    def json_request(self, method, endpoint, params, headers={}, **parameter):

        url = f("https://graph.microsoft.com/v1.0/{endpoint}")

        _params = {}
        if params is not None:
            _params.update(**params)
        _params.update(**parameter)

        _headers = self.headers()
        _headers.update(headers)

        logger.debug("request: %s %s: %s", method, url, _params)

        return getattr(requests, method)(url, json=_params, headers=_headers)
