from tornado.ncss import Server, ncssbook_log
import tornadotesting
from template import render_template
from db import User

def render_file(filename, context):
    """
    Reads a template file and pases it through the template engine.

    >>>tornadotesting.run(render_file, 'profile.html', '{"name":"sandy"}')
    My name is sandy

    """
    with open(filename) as f:

        template = f.read()

        return render_template(template, context)


def view_profile(request, username):
    """
    >>> tornadotesting.run(view_profile, 'alice')
    'My username is sandy'
    """

    user = User.get_by_username(username)

    template = "My username is {{ name }}"
    context = {'name':user.username}

    request.write(render_file('profile.html', context))





if __name__ == '__main__':
    server = Server()
    server.register(r'/profile/([a-z]+)', view_profile)
    server.run()
