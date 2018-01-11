from tornado.ncss import Server, ncssbook_log
import tornadotesting
from template import render_template
from db.db import User

def view_profile(request):
    """
    >>> tornadotesting.run(view_profile)
    'My username is sandy'
    """

    user = User.get_by_username("sandy")
    
    template = "My username is {{ name }}"
    context = {'name':user.username}

    request.write(render_template(template, context))
    

    


if __name__ == '__main__':
    server = Server()
    server.register(r'/', view_profile)
    server.run()
