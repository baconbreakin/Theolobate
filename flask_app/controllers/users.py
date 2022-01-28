from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return redirect('/sign_in')

@app.route('/sign_in')
def sign_in():
    return render_template("sign_in.html")

@app.route('/login', methods=['POST'])
def login():
    data = {"email": request.form["email"]}
    user_in_db = User.get_by_email(data)
    valid_login = True
    if not user_in_db:
        flash("Invalid Email")
        valid_login = False
    if len(request.form["password"]) > 0:
        if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
            flash("Invalid Password")
            valid_login = False
    else:
        flash("Invalid Password")
        valid_login = False
    if valid_login == False:
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')

@app.route('/sign_up')
def sign_up():
    return render_template("sign_up.html")

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/sign_up')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if len(session) < 1:
        return redirect('/')
    data = {"id": session['user_id']}
    user_in_db = User.get_by_id(data)
    posts = Post.get_all()
    return render_template("dashboard.html", posts = posts, user_in_db = user_in_db)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')