from tornado.ncss import Server, ncssbook_log
import tornadotesting
from template import render_template
from db import User, Squad, DbObject, SquadMembers
from datetime import date

def get_form_data(request, fields):
    output = {}
    for field in fields:
        if not request.get_field(field):
            return
        output[field] = request.get_field(field)

    return output

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
    >>> tornadotesting.run(create_profile, fields={'username': 'alice',
    ...     'password': 'test', 'description': 'test', 'location': 'test',
    ...     'birthdate': 'test'})
    Redirect('/profiles/alice/')
    """
    accept_fields = ['username', 'password', 'description', 'location', 'birthdate']
    data = get_form_data(request, accept_fields)
    if not data:
        request.write('You must complete all fields.')
        return
    data['image'] = ''
    user = User.create(**data)
    request.redirect('/profiles/{}/'.format(user.username))

def list_squads(request):
    """
    >>> html = tornadotesting.run(list_squads)
    >>> assert 'Squads' in html, html
    """
    all_squads = Squad.get_all()
    context = {"squads":all_squads}
    request.write(render_file("list_squads.html", context))


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
    >>> html = tornadotesting.run(view_squad, 'ateam')
    >>> assert 'ateam' in html, html
    """
    squad = Squad.get_by_squadname(name)

    applicants = SquadMembers.get_all(squad.squadname)

    user_placeholder = 'ames'

    context = {
        'Squad':name,
        'leader':squad.leader,
        'date':squad.squad_date,
        'time':squad.squad_time,
        'location':squad.location,
        'required_numbers': str(squad.capacity),
        'description':squad.description,
        'current_user':'alice',
        'applicants':applicants,
        'current_user':user_placeholder
    }

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
    'You must complete all fields.'
    >>> tornadotesting.run(create_squad, fields={
    ...     'squadname': 'alice', 'capacity': '4', 'squad_date': date.today(),
    ...     'description': 'blah', 'location': 'Australia', 'leader': 'sandy',
    ...     'squad_time': '6:33' })
    'squad created with name alice'

    """

    accept_fields = ['squadname', 'capacity', 'squad_date', 'description', 'location', 'leader', 'squad_time']
    data = get_form_data(request, accept_fields)
    if not data:
        request.write('You must complete all fields.')
        return
    squad = Squad.create(**data)
    request.write('squad created with name {}'.format(squad.squadname))

def accept_reject_squad_member(request, name):
    """
    >>> tornadotesting.run(accept_squad_member, 'ateam', fields={'username': 'James'})
    'Accepted'
    >>> tornadotesting.run(accept_squad_member, 'ateam', fields={'username': 'bruce'})
    'Insufficient permissions'
    """

    squad = Squad.get_by_squadname(name)

    print(request.get_fields())

    form_data = request.get_fields()

    username = sorted(form_data.keys())[0]

    status = 0

    if form_data[username][0] == "accept":
        status = 2

    if form_data[username][0] == "reject":
        status = 1


    status = SquadMembers.change_status(new_status=status, squadname=name, username=username)
    request.redirect('/squads/{}/'.format(squad.squadname))


def apply_to_squad(request, name):
    """
    >>> tornadotesting.run(apply_to_squad, 'ateam', fields={'username': 'alice'})
    '0'
    """
    user_placeholder = ''
    status = SquadMembers.apply(squadname=name, username=user_placeholder)
    request.redirect('/squads/{}/'.format(name))

def redirect_root(request):
    """
    >>> tornadotesting.run(redirect_root)
    Redirect('/squads/')
    """
    request.redirect('/squads/')


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
server.register(r'/profiles/([a-z]+)/?', view_profile)
server.register(r'/register/?', create_profile_page, post=create_profile)
server.register(r'/squads/?', list_squads, post=create_squad)
server.register(r'/squads/([a-z]+)/?', view_squad)
server.register(r'/create-squad/?', show_create_squad_page)
server.register(r'/squads/([a-z]+)/accept-reject/?', accept_reject_squad_member)
server.register(r'/squads/([a-z]+)/apply/?', apply_to_squad)
server.register(r'/', redirect_root)
server.register(r'/login/?', login_page, post=process_login )

DbObject.start_database()

if __name__ == '__main__':
    server.run()
