from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():

    return render_template('register.html')

@app.route('/admin-login')
def login_admin():
    return render_template('admin-login.html')
