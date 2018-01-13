from io import StringIO

class Redirect:
    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return 'Redirect(%r)' % (self.url,)

class RequestHandler:
    def __init__(self, fields):
        super().__init__()
        self._fields = fields
        self._output = StringIO()
        self._redirect = None

    def get_field(self, name, default=None):
        return self._fields.get(name, default)

    def get_fields(self):
        return self._fields

    def write(self, data):
        self._output.write(data)

    def redirect(self, url):
        self._redirect = Redirect(url)

    def _get_result(self):
        return self._redirect or self._output.getvalue()

def run(fn, *args, **kwargs):
    fields = kwargs.pop('fields', {})
    if kwargs:
        raise ValueError('invalid keyword arguments: {}'.format(kwargs))
    request = RequestHandler(fields)
    fn(request, *args)
    return request._get_result()

