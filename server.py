from tornado.ncss import Server, ncssbook_log
import tornadotesting
from template import render_template
from db import User, Squad, DbObject, SquadMembers
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
    request.write(render_file("test-register.html", context))

def create_profile(request):
    """
    >>> tornadotesting.run(create_profile, fields={'username': 'alice'})
    'You created a user called alice'
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
    request.write("You created a user called {}".format(user.username))

def list_squads(request):
    """
    >>> html = tornadotesting.run(list_squads)
    assert 'Squads' in html, html
    """
    all_squads = Squad.get_all()
    context = {"squads":all_squads}
    request.write(render_file("allSquads.html", context))


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
    squad = Squad.get_by_squadname(name)
    context = {'Squad':name, 'host':squad.leader, 'date':squad.squad_date, 'time':squad.squad_time, 'location':squad.location, 'required_numbers': str(squad.capacity), 'description':squad.description}
    request.write(render_file('squad_details.html', context))


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

def login_page(request):
    if is_logged_in(request):
        request.redirect(r'/squads/')
    else:
        context = {}
        request.write(render_file('test-login.html', context))

def process_login(request):
    luser = request.get_field('username')
    lpass = request.get_field('password')
    users = User.get_all()
    is_valid_user = False
    for user in users:
        if user.username == luser:
            if user.password ==lpass:
                is_valid_user = True
    if is_valid_user:
        request.set_secure_cookie('squadify-login', 'Logged In')
        request.write('You have successfully logged in! Well done! Good on you! Is the sarcasm obvious yet?')
    else:
        request.write("Aww, too bad, your username or password was incorrect, maybe try agian? or sign up if you're trying to sign up on the login page like a gumbo.")

def is_logged_in(request):
    if request.get_secure_cookie('squadify-login'):
        return True
    else:
        return False

server = Server()
server.register(r'/profiles/([a-z]+)/', view_profile)
server.register(r'/register/', create_profile_page, post=create_profile)
server.register(r'/squads/', list_squads, post=create_squad)
server.register(r'/squads/([a-z]+)/', view_squad)
server.register(r'/create-squad/', show_create_squad_page)
server.register(r'/squads/([a-z]+)/accept/', accept_squad_member)
server.register(r'/squads/([a-z]+)/reject/', reject_squad_member)
server.register(r'/squads/([a-z]+)/apply/', apply_to_squad)
server.register(r'/login/', login_page, post=process_login )

if __name__ == '__main__':
    DbObject.start_database()
    server.run()
