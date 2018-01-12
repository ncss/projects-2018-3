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


def list_squads(request):
    """
    >>> tornadotesting.run(list_squads)
    'This page lists all squads'
    """
    
    request.write('This page lists all squads')
    

def view_squad(request, name):
    """
    >>> tornadotesting.run(view_squad, 'ateam')
    'This is the squad page for ateam'
    
    """
    
    request.write('This is the squad page for {}'.format(name))


def show_create_squad_page(request):
    """
    >>> tornadotesting.run(show_create_squad_page)
    'This page creates a "create a squad" form'
    """
    
    request.write('This page creates a "create a squad" form')

def create_squad(request):
    """
    >>> tornadotesting.run(create_squad)
    'This page creates a squad'
    """
    
    request.write('This page creates a squad')
    
def accept_squad_member(request, name):
    """
    >>> tornadotesting.run(accept_squad_member, 'ateam')
    'This page accepts ateam'
    """
    
    request.write('This page accepts {}'.format(name))

def reject_squad_member(request, name):
    """
    >>> tornadotesting.run(reject_squad_member, 'ateam')
    'This page reject ateam'
    """
    
    request.write('This page reject {}'.format(name))

def apply_to_squad(request, name):
    """
    >>> tornadotesting.run(apply_to_squad, 'ateam')
    'This the page to apply to join ateam'
    """

    request.write('This the page to apply to join {}'.format(name))

server = Server()
server.register(r'/profiles/([a-z]+)/', view_profile)
server.register(r'/register/', create_profile)
server.register(r'/squads/', list_squads, post=create_squad)
server.register(r'/squads/([a-z]+)/', view_squad)
server.register(r'/create-squad/', show_create_squad_page)
server.register(r'/squads/([a-z]+)/accept/', accept_squad_member)
server.register(r'/squads/([a-z]+)/reject/', reject_squad_member)
server.register(r'/squads/([a-z]+)/apply/', apply_to_squad)

if __name__ == '__main__':
    server.run()
