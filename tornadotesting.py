from io import StringIO

def run(fn, *args):
    request = StringIO()
    fn(request, *args)
    return request.getvalue()
    
