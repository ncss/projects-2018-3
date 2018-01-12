from tornado.ncss import Server, ncssbook_log
import tornadotesting
from template import render_template
from db import User

def render_file(filename, context):
    """
    Reads a template file and pases it through the template engine.

    >>> render_file('test-render-file.html', {"name":"sandy"})
    'My name is sandy'
    """
    with open("templates/" + filename) as f:

        template = f.read()

        return render_template(template, context)


def view_profile(request, username):
    """
    >>> html = tornadotesting.run(view_profile, 'alice')
    >>> "sandy" in html
    True
    """

    user = User.get_by_username(username)

    template = "My username is {{ name }}"
    context = {'name':user.username}

    request.write(render_file('profile.html', context))


def create_profile(request):
    """
    >>> tornadotesting.run(create_profile)
    'This is the create user page'
    
    """
    
    request.write('This is the create user page')
    

server = Server()
server.register(r'/profiles/([a-z]+)', view_profile)
server.register(r'/register', create_profile)

if __name__ == '__main__':
    server.run()
