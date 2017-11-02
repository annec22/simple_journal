import json

from flask import \
    Flask, \
    render_template, \
    session, \
    redirect, \
    url_for, \
    request, make_response, Response

from src.common.database import Database
from src.models.entry import Entry
from src.models.user import User

app = Flask(__name__)
app.secret_key = "anne"

@app.before_first_request
def initialize_database():
    Database.initialize()

@app.route('/')
def home_template():
    if is_logged_in():
        user = User.get_user_by_username(session['username'])

        entries = user.get_user_entries_by_user_id()

        return render_template('home.html', name=user.name, active=is_logged_in(), entries=entries, journal_active="active")
    else:
        return redirect(url_for('login_template'))

@app.route('/about')
def about_template():
    return render_template('about.html', active=is_logged_in(), about_active="active")

@app.route('/login')
def login_template():
    if is_logged_in():
        return redirect(url_for('home_template'))
    else:
        return render_template('login.html')


@app.route('/register')
def register_template():
    if is_logged_in():
        return redirect(url_for('home_template'))
    else:
        return render_template('register.html')


@app.route('/auth/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']

    if User.is_valid_login(username, password):
        User.login_user(username)

    return redirect(url_for('home_template'))

@app.route('/auth/register', methods=['POST'])
def register_user():
    name = request.form['name']
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    User.register_user(name, username, email, password)
    return redirect(url_for('home_template'))

@app.route('/logout')
def user_logout():
    User.logout()
    return redirect(url_for('home_template'))

@app.route('/new_entry', methods=['POST'])
def new_entry():
    user = User.get_user_by_username(session['username'])
    title = request.form['title']
    content = request.form['content']
    date = request.form['date-event']
    user.new_entry(user._id, title, content, date)

    return redirect(url_for('home_template'))

@app.route('/save_to_local')
def get_json_entries():
    user = User.get_user_by_username(session['username'])
    entries = user.get_user_entries_by_user_id()
    data = [Entry(**entry).json() for entry in entries]
    data = json.dumps([Entry(**entry).json() for entry in entries])
    response = make_response()
    response.data = data
    response.mimetype = "application/json"
    response.headers['content-disposition']= 'attachment;filename="entries.json"'
    return response



def is_logged_in():
    return 'username' in session and session['username'] is not None

if __name__ == "__main__":
    app.run(debug=True)