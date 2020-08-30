import requests
from itertools import count
import ujson

DEFAULT_HTTP_TIMEOUT = 120
DEFAULT_RPC_PORT = 7783


class MMProxy:
    _ids = count(0)

    def __init__(self, conf_dict=None, timeout=DEFAULT_HTTP_TIMEOUT):
        self.timeout = timeout
        self.config = conf_dict
        self.userpass = conf_dict.get('userpass')
        if not conf_dict.get('rpcport'):
            self.config['rpcport'] = DEFAULT_RPC_PORT

    def __getattr__(self, req):
        _id = next(self._ids)
        upass = self.userpass

        def call(**params):
            if req != 'batch':
                post_val = {
                    'jsonrpc': '2.0',
                    'userpass': upass,
                    'method': req,
                    'id': _id
                }
                for param, value in params.items():
                    post_val.update({param: value})
            else:
                post_val = []
                for key in params:
                    post_dict = {
                        'jsonrpc': '2.0',
                        'userpass': upass,
                        'method': params.get(key).get('method'),
                        'id': _id
                    }
                    for param, value in params.get(key).items():
                        post_dict.update({param: value})
                    post_val.append(post_dict)
            url = 'http://%s:%s' % (self.config['rpchost'], self.config['rpcport'])
            post_data = ujson.dumps(post_val)
            try:
                resp = requests.post(url, data=post_data, timeout=self.timeout).json()
            except ValueError:
                resp = str(requests.post(url, data=post_data, timeout=self.timeout).content)
            return resp

        return call
