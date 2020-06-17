import os
import passwordmeter
from flask import Flask, session, render_template, jsonify, request, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import sys
app = Flask(__name__)

# secret KEY
app.config['SECRET_KEY'] = '\x84}r\n\xdc\x88\xf8\xf3\x07\x06_*\x9a\xd0\x80\xe88Z\xea\xc6\x83\xbb\xf7\x0e'


# api
# res = request.get("https://www.goodreads.com/book/review_counts.json",
#                  params={"key": "KEY", "isbns": "9781632168146"})
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
# login_manager = LoginManager()
# login_manager.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    result = None
    if request.method == 'POST':
        uname = request.form.get("uname")
        uemail = request.form.get("uemail")
        upass = request.form.get("upass")
        urepass = request.form.get("urepass")
        strength, improvements = passwordmeter.test(upass)
        if uname is None or uemail is None or upass is None or urepass is None:
            result = "some fields are vacent,fill the form completely."
            return render_template('signup.html', result=result)  # , improvements=improvements)
        elif urepass != upass:
            result = "password doesn't match, try again."
            return render_template('signup.html', result=result)  # , improvements=improvements)
        elif strength < 0.5:
            result = "password is very weak."
            return render_template('signup.html', result=result,
                                   improvements=improvements)

        elif strength < 0.8:
            result = "password is weak."
            return render_template('signup.html', result=result,
                                   improvements=improvements)

        elif strength > 0.8:
            return redirect(url_for('login'))
    return render_template('signup.html')

#
# @app.route('/signing', methods=['POST'])
# def signing():
#     if request.method == 'POST':
#         name = request.form.get("name")
#
#         strength, improvements = passwordmeter.test(sys.argv[1])
#         if strength < 0.5:
#             result = "password is very weak."
#             return render_template('signup.html', improvements=improvements)
#
#         elif strength < 1.0:
#             result = "password is weak."
#             return render_template('signup.html', improvements=improvements)
#
#         elif strength > 1.0:
#             return render_template('success.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))
