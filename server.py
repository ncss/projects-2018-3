from tornado.ncss import Server, ncssbook_log
import tornadotesting
from template import render_template
from db import User, Squad, DbObject#, SquadMembers
from datetime import date

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
    >>> assert "James" in html, html
    >>> assert "42" in html, html
    >>> assert "Sydney" in html, html
    """

    user = User.get_by_username(username)

    #Age code for when DB sends an actual date object
    #age = date.today().year - user.birthdate.year


    context = {'username':user.username, 'age':'42', 'loc':user.location, 'description':user.description }


    request.write(render_file('profile.html', context))


def create_profile_page(request):
    """
    >>> html = tornadotesting.run(create_profile_page)
    >>> assert "description" in html, html
    >>> assert "submit" in html, html
    """
    context={}
    request.write(render_file("register.html", context))

def create_profile(request):
    """
    >>> tornadotesting.run(create_profile, fields={'username': 'alice'})
    Redirect('/profiles/alice/')
    """
    user_data = {}
    user_data["username"] = request.get_field("username")
    user_data["password"] = request.get_field("password")
    user_data["description"] = request.get_field("description")
    user_data["location"] = request.get_field("location")
    user_data["birthdate"] = request.get_field("birthdate")
    user_data["image"] = request.get_field("image")
    #print(user_data)

    user = User.create(**user_data)
    request.redirect("/profiles/{}/".format(user.username))

def list_squads(request):
    """
    >>> tornadotesting.run(list_squads)
    'aaa 10 15/1/2018 This is a squad'

    """
    all_squads = Squad.get_all()
    context = {"events":all_squads}
    request.write(render_file("squad-list.html", context))




    #names = []
    #capacity = []
    #event_date = []
    #description = []
    #for squad in all_squads:
        #names.append(squad.name)
        #capacity.append(str(squad.capacity))
        #event_date.append(str(squad.event_date))
        #description.append(squad.description)
    #request.write(','.join(names) +' '+ ','.join(capacity) +' '+ ','.join(event_date) +' '+ ','.join(description))

def view_squad(request, name):
    """
    >>> tornadotesting.run(view_squad, 'ateam')
    'This is the squad page for aaa'
    """
    squad = Squad.get_by_name(name)




    request.write('This is the squad page for {}'.format(squad.name))


def show_create_squad_page(request):
    """
    >>> tornadotesting.run(show_create_squad_page)
    'This page creates a "create a squad" form'
    """

    request.write('This page creates a "create a squad" form')

def create_squad(request):
    """
    >>> tornadotesting.run(create_squad)
    'Go Away!'
    >>> tornadotesting.run(create_squad, fields={
    ...     'squadname': 'alice', 'capacity': '4', 'squad_date': date.today(),
    ...     'description': 'blah', 'location': 'Australia', 'leader': 'sandy',
    ...     'squad_time': '6:33' })
    'squad created with name alice'

    """
    data = request.get_fields()
    accept_fields = ['squadname', 'capacity', 'squad_date', 'description', 'location', 'leader', 'squad_time']
    if sorted(data.keys()) != sorted(accept_fields):
        request.write('Go Away!')
        return
    squad = Squad.create(**data)
    request.write('squad created with name {}'.format(squad.squadname))



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
    >>> tornadotesting.run(apply_to_squad, fields={'current_user': 'alice'})
    'Pending...'
    """
    data = request.get_fields()
    accept_fields = ['current_user']
    if sorted(data.keys()) != sorted(accept_fields):
        request.write('Go Away!')
        return
    status = SquadMembers.apply(name, **data)
    request.write(status)

server = Server()
#server.register(r'/')
server.register(r'/profiles/([a-z]+)/', view_profile)
server.register(r'/register/', create_profile_page, post=create_profile)
server.register(r'/squads/', list_squads, post=create_squad)
server.register(r'/squads/([a-z]+)/', view_squad)
server.register(r'/create-squad/', show_create_squad_page)
server.register(r'/squads/([a-z]+)/accept/', accept_squad_member)
server.register(r'/squads/([a-z]+)/reject/', reject_squad_member)
server.register(r'/squads/([a-z]+)/apply/', apply_to_squad)

if __name__ == '__main__':
    DbObject.start_database()
    server.run()
