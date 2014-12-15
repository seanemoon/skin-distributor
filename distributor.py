# imports for flask and our database
import sqlite3
from flask import *
from wtforms import *
from models.Account import *
from models.Event import *

# Configuring our flask app
app = Flask(__name__)
app.config.from_envvar('CONFIG', silent=False)

# Returns an open database connection
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

# Ensures that our request object holds an open database connection
@app.before_request 
def before_request():
    g.db = connect_db()

# Closes the database connection after a request
@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def is_logged_in():
    return 'email' in session

# Redirects the user to the login page if the user is not logged in.
# Otherwise, this is a no-op.
def ensure_logged_in():
    if not is_logged_in():
        flash('Please log in.')
        return redirect(url_for('login_or_register'))

@app.route('/events/')
def events():
    ensure_logged_in()
    events = Event.get_events_for(session['account_id'], g.db)
    return render_template('events.html', events=events)

class EventForm(Form):
    name = TextField('Email Address', [
        validators.Required()
    ])

# TODO(seanraff): finish this.
@app.route('/events/add/')
def add_event():
    result = {'success': False}
    if is_logged_in():
        name = request.args.get('name', None)
        event = Event.create(name, session['account_id'], g.db)
        result['success'] = True
    return jsonify(result)


class CreateEventForm(Form):
    sender = TextField('Sender', [validators.Required()])
    subject = TextField('Subject', [validators.Required()])
    header = TextField('Header', [validators.Required()])
    body = TextAreaField('Body', [validators.Required()])


@app.route('/events/create/', methods=['POST', 'GET'])
def create_event():
    ensure_logged_in()
    if request.method == 'GET':
        form = CreateEventForm()
        return render_template('create_event.html', form=form)
    else:
        pass

@app.route('/events/delete')
def delete_event():
    result = {'success': False}
    if is_logged_in():
        id = request.args.get('id', None)
        Event.delete(id, g.db)
        result['success'] = True
    return jsonify(result)

class LoginForm(Form):
    email = TextField('Email Address', [
        validators.Length(min=3, max=360),
        validators.Required()
    ])
    password = PasswordField('New Password', [
        validators.Length(min=6, max=100),
        validators.Required()
    ])

class RegistrationForm(Form):
    email = TextField('Email Address', [
        validators.Length(min=3, max=360),
        validators.Required()
    ])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.Length(min=6, max=100),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password', [
        validators.Required()
    ])

@app.route('/')
def login_or_register():
    forms = {}
    forms['register'] = RegistrationForm()
    forms['login'] = LoginForm()
    return render_template('login_or_register.html', forms=forms)

@app.route('/register', methods=['POST'])
def register():
    form = RegistrationForm(request.form)
    if form.validate():
        account = Account.create(form.email.data, form.password.data, g.db)
        flash('Thanks for registering')
        session['email'] = account.email
        session['account_id'] = account.id
        return redirect(url_for('events', email=account.email))
    else:
        return redirect(url_for('login_or_register'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_or_register'))

@app.route('/login', methods=['POST'])
def login():
    form = LoginForm(request.form)
    if form.validate():
        account = Account.login(form.email.data, form.password.data, g.db)
        if account is not None:
            session['email'] = account.email
            session['account_id'] = account.id
            return redirect(url_for('events', email=account.email))
        else:
            flash('Invalid email or password.')
            return redirect(url_for('login_or_register'))
    flash('Invalid email or password.')
    return redirect(url_for('login_or_register'))

if __name__ == '__main__':
    app.run()
