from datetime import datetime

from flask import Flask, render_template, request, session, redirect, url_for, g, flash
from werkzeug.datastructures import MultiDict
from flask_wtf import csrf

import database_mangement as db_manger
from confirmIdentity import confirmIdentity
from edit_profile_form import edit_profile_form
from register_user import registerUserForm
from login import login_form
from cryptography.fernet import Fernet
from flask_socketio import SocketIO

import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'good_ol_secret_key'
# makes sure CSRF doesnt go out of context
csrf.CSRFProtect(app)
socketio = SocketIO(app)

# fernet will be used to encrypt the password
# look up documentation, its pretty simple tbh
key = Fernet.generate_key()
f = Fernet(key)


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = db_manger.get_unique_user_by_id(session['user_id'])
        if len(user) > 0:
            g.user = user[0]


# main page of application
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=('GET', 'POST'))
def register():
    # create form
    form = registerUserForm()
    # if validation passes
    if form.validate_on_submit():
        # get data from form
        fn = form['first_name'].data
        ln = form['last_name'].data
        dob = form['dob'].data
        un = form['username'].data
        # pw = f.encrypt(str.encode(form['password'].data))
        pw = form['password'].data
        gd = form['gender'].data
        # insert into database
        db_manger.insert_user(un, pw, fn, ln, dob, gd)
        # go back home
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = login_form()
    if form.validate_on_submit():
        # remove current session
        session.pop('user_id', None)
        # get form data
        username = form['username'].data
        password = form['password'].data
        # retrieve user from database if exists
        user = db_manger.get_unique_user(username)
        # check if user exists and password matches
        if len(user) > 0 and user[0][2] == password:
            # set up session with user_id (id column in db)
            session['user_id'] = user[0][0]
            # redirect to profile page
            return redirect(url_for('profile'))
        # if no user, redirect back to login page
        flash("Username or Password invalid, please try again.")
        return redirect(url_for('login'))
    # if method is not post, go to login.hmtl
    return render_template('login.html', form=form)


@app.route('/signout')
def signout():
    # logs out of session, returns user back home
    session.pop('user_id', None)
    return redirect(url_for('home'))


@app.route('/profile')
def profile():
    # profile page shows details of user
    if not g.user:
        # if not logged in, redirect them to the login page
        return redirect(url_for('login'))
    return render_template('profile.html', g=g)


@app.route('/confirm_identity', methods=["GET", "POST"])
def confirm_identity():
    form = confirmIdentity()
    if form.validate_on_submit():
        password = form['password'].data
        print(password)
        if g.user[2] != password:
            return redirect(url_for('confirm_identity'))
        return redirect(url_for('edit_profile'))
    return render_template('confirm_identity.html', g=g, form=form)


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    # setting up default fields for user data
    form = edit_profile_form(
        formdata=MultiDict({'first_name': g.user[4], 'last_name': g.user[5], 'dob': g.user[6], 'gender': g.user[7]}))
    if form.validate_on_submit():
        # stuff to update the database

        return redirect(url_for('profile'))

    return render_template("edit_profile.html", form=form)


# page for drawing
@app.route('/draw', methods=['GET', 'POST'])
def draw():
    if request.method == 'GET':
        return render_template('draw.html')
    if request.method == 'POST':
        id = str(uuid.uuid4())
        wbname = request.form['wb_name']
        data = request.form['save_cdata']
        canvas_image = request.form['save_image']

        # db_manger.insert_drawing(id, wbname, user, data, canvas_image)

        return redirect(url_for('index'))


@app.route('/load', methods=['GET', 'POST'])
def load():
    return

@app.route('/session')
def sessions():
    return render_template('session.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

# @app.route('/save', methods=['GET','POST'])
# def save():


if __name__ == '__main__':
    app.run('localhost', debug=True)

# (id, WBName, Username, Timestamp, data, canvas_image)
