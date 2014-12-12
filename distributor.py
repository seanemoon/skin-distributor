# imports for flask and our database
import sqlite3
from flask import *

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

@app.route('/')
def show_entries():
    return render_template('login.html')

if __name__ == '__main__':
    app.run()
