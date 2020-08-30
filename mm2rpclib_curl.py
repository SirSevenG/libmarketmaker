import ujson
from itertools import count
from pycurl import Curl
from io import BytesIO as StringIO

DEFAULT_HTTP_TIMEOUT = 120
DEFAULT_RPC_PORT = 7783


class MMProxy:
    _ids = count(0)

    def __init__(self, conf_dict=None, timeout=DEFAULT_HTTP_TIMEOUT):
        self.config = conf_dict
        self.userpass = conf_dict.get('userpass')
        if not conf_dict.get('rpcport'):
            self.config['rpcport'] = DEFAULT_RPC_PORT
        self.conn = self.prepare_connection(self.config, timeout=timeout)

    def __getattr__(self, req):
        conn = self.conn
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
            postdata = ujson.dumps(post_val)
            body = StringIO()
            conn.setopt(conn.WRITEFUNCTION, body.write)
            conn.setopt(conn.POSTFIELDS, postdata)
            conn.perform()
            try:
                resp = ujson.loads(body.getvalue())
            except ValueError:
                resp = str(body.getvalue().decode('utf=8'))
            return resp

        return call

    @classmethod
    def prepare_connection(cls, conf, timeout=DEFAULT_HTTP_TIMEOUT):
        url = 'http://%s:%s' % (conf['rpchost'], conf['rpcport'])
        conn = Curl()
        conn.setopt(conn.CONNECTTIMEOUT, timeout)
        conn.setopt(conn.TIMEOUT, timeout)
        conn.setopt(conn.URL, url)
        conn.setopt(conn.POST, 1)
        return conn
