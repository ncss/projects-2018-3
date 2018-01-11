from tornado.ncss import Server, ncssbook_log
import tornadotesting

def view_profile(request):
    """
    >>> tornadotesting.run(view_profile)
    'Hi'
    """
    request.write('Hi')


if __name__ == '__main__':
    server = Server()
    server.register(r'/', view_profile)
    server.run()
