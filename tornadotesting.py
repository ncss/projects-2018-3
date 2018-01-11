from io import StringIO

def run(fn):
    request = StringIO()
    fn(request)
    return request.getvalue()
    
