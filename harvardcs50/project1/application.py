import os

import requests
import passwordmeter
from flask import Flask, session, render_template, jsonify, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# secret KEY
app.secret_key

# api
res = requests.get("https://www.goodreads.com/book/review_counts.json",
                   params={"key": "KEY", "isbns": "9781632168146"})
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
# passwordmeter

# flask login
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/signup', methods=['GET'])
def signup():

    name = request.form.get("name")

    strength, improvements = passwordmeter.test(sys.argv[1])
   if strength < 0.5:
        result = "password is very weak."
        return render_template('signup', improvements)

    elif strength < 1.0:
        result = "password is weak."
        return render_template('signup', improvements)

    elif strength > 1.0:
        return render_template('success.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))
