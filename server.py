from tornado.ncss import Server, ncssbook_log
import tornadotesting
from template import render_template

def view_profile(request):
    """
    >>> tornadotesting.run(view_profile)
    'My name is Isaac'
    """

    template = "My name is {{ name }}"
    context = {'name':'Isaac'}

    request.write(render_template(template, context))
    

    


if __name__ == '__main__':
    server = Server()
    server.register(r'/', view_profile)
    server.run()
