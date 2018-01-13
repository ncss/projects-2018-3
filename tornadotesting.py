import contextlib
import io

_sessions = [None]

@contextlib.contextmanager
def session():
    _sessions.append({})
    yield
    _sessions.pop()

def _current_session():
    session = _sessions[-1]
    if session is None:
        return {}
    return session

class Redirect:
    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return 'Redirect(%r)' % (self.url,)

class RequestHandler:
    def __init__(self, fields):
        super().__init__()
        self._fields = fields
        self._output = io.StringIO()
        self._redirect = None
        self._cookies = _current_session()

    def get_field(self, name, default=None):
        return self._fields.get(name, default)

    def get_fields(self):
        return self._fields

    def write(self, data):
        self._output.write(data)

    def redirect(self, url):
        self._redirect = Redirect(url)

    def get_secure_cookie(self, name, value=None):
        return self._cookies.get(name, value)

    def set_secure_cookie(self, name, value, **kwargs):
        if isinstance(value, str):
            value = value.encode('utf-8')
        self._cookies[name] = value

    def _get_result(self):
        return self._redirect or self._output.getvalue()

def run(fn, *args, **kwargs):
    fields = kwargs.pop('fields', {})
    if kwargs:
        raise ValueError('invalid keyword arguments: {}'.format(kwargs))
    request = RequestHandler(fields)
    fn(request, *args)
    return request._get_result()

