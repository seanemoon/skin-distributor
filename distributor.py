# imports for flask and our database
import sqlite3
from flask import *
from wtforms import *
from models.Account import *

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
def show_entries():
    form = RegistrationForm(request.form)
    return render_template('login.html', form=form)

@app.route('/events/<email>')
def events(email):
    return "hi"

@app.route('/register', methods=['POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = Account(form.email.data, form.password.data)
        flash('Thanks for registering')
        user.add(g.db)
        return redirect(url_for('events', email=user.email))
    return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run()
