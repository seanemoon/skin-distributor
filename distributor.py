# imports for flask and our database
import sqlite3
import os
from flask import *
from wtforms import *
from werkzeug import secure_filename
from models.Account import *
from models.Event import *
from models.Template import *
from models.Code import *
from models.Recipient import *

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
    return session.get("email", None) is not None
def not_logged_in():
    return not is_logged_in() 

# Redirects the user to the login page if the user is not logged in.
# Otherwise, this is a no-op.
def request_login():
    return redirect(url_for('login_or_register'))


ALLOWED_EXTENSIONS = set(['txt', 'xls', 'csv'])
def allowed_file(filename):
    print '.' in filename
    print filename.rsplit('.',1)[1]
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        f = request.files['0']
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            

@app.route('/codes/clear')
def clear_codes():
    result = {'success': False}
    if is_logged_in():
        event_id = request.args.get('event_id', None)
        Code.clear(event_id, session['account_id'], g.db)
        result = {'success': True}
    return jsonify(result)


@app.route('/recipients/clear')
def clear_recipients():
    result = {'success': False}
    if is_logged_in():
        event_id = request.args.get('event_id', None)
        Recipient.clear(event_id, session['account_id'], g.db)
        result = {'success': True}
    return jsonify(result)

@app.route('/events/')
def events():
    if not_logged_in(): return request_login();
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
        result['name'] = name
        result['id'] = event.id
    return jsonify(result)

@app.route('/events/<event_id>')
def view_event(event_id):
    if not_logged_in():
        return request_login();
    event = Event.fetch(session['account_id'], event_id, g.db)
    template = Template.fetch(event_id, session['account_id'], g.db)
    code_info = Code.fetch_info(event_id, session['account_id'], g.db)
    num_recipients = Recipient.num_recipients(event_id, g.db)
    return render_template('event.html', event=event, template=template, \
            code_info=code_info, num_recipients=num_recipients)

@app.route('/events/create')
def create_event():
    if not_logged_in(): return request_login();
    event = Event.create(session['account_id'], g.db)
    return redirect(url_for('view_event', event_id=event.id))

class CreateTemplateForm(Form):
    sender = TextField('Sender', [validators.Required()])
    subject = TextField('Subject', [validators.Required()])
    header = TextField('Header', [validators.Required()])
    body = TextAreaField('Body', [validators.Required()])
    code_types = HiddenField('Code Types', [validators.Optional()])

@app.route('/template/view/<event_id>')
def view_template(event_id):
    if not_logged_in(): return request_login();
    template = Template.fetch(event_id, session['account_id'], g.db)

    print (event_id, session['account_id'])
    print template
    return render_template('email_template.html', template=template)

@app.route('/template/edit/<event_id>', methods=['POST', 'GET'])
def edit_template(event_id):
    if not_logged_in(): return request_login();
    if request.method == 'GET':
        template = Template.fetch(event_id, session['account_id'], g.db)
        form = CreateTemplateForm( \
                sender=template.sender, \
                subject=template.subject, \
                header=template.header, \
                body=template.body)
        return render_template('create_template.html', \
                form=form, event_id=event_id, update=True, code_types=template.code_types)
    else:
        form = CreateTemplateForm(request.form)
        if form.validate():
            template = Template.fetch(event_id, session['account_id'], g.db)
            template.update(
                form.sender.data, \
                form.subject.data, \
                form.header.data, \
                form.body.data, \
                form.code_types.data, \
                g.db \
            )
            return redirect(url_for('view_event', event_id=event_id))
        else:
            return redirect(url_for('create_template', event_id=event_id))



@app.route('/template/create/<event_id>', methods=['POST', 'GET'])
def create_template(event_id):
    if not_logged_in(): return request_login();
    if request.method == 'GET':
        form = CreateTemplateForm()
        return render_template('create_template.html', form=form, event_id=event_id)
    else:
        form = CreateTemplateForm(request.form)
        if form.validate():
            template = Template.create(
                event_id, \
                form.sender.data, \
                form.subject.data, \
                form.header.data, \
                form.body.data, \
                form.code_types.data, \
                g.db \
            )
            return redirect(url_for('view_event', event_id=event_id))
        else:
            return redirect(url_for('create_template', event_id=event_id))



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
        return redirect(url_for('events'))
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
