# this is where you put all your routes
from flask_app import app, render_template, redirect, request, bcrypt, session, flash

#import models, replace xxxx with necessary model file (User)
from flask_app.models.user import User

#default route to index
@app.route("/")
def index():
    return render_template("index.html")

#register user
@app.route("/register", methods=['POST'])
def add_new_user():
    print(request.form)

    #Check if user already exists
    user = User.get_by_email(request.form)
    if user:
        flash("User already exists, please log in")
        return redirect("/")
        
    # validate our user
    if not User.validate_user(request.form):
        return redirect('/')
    
    # validation completed, now we  hash the password
    hashed_pw = bcrypt.generate_password_hash(request.form['password'])
    print(hashed_pw)
    
    # save the user to the database
    user_data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': hashed_pw
    }
    user_id = User.create_new_user( user_data)
    
    # log in the user
    session['user_id'] = user_id
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']
    # TODO redirect user to app
    return redirect('/recipes')


# get login info and verify
@app.route('/login', methods=['post'])
def login():
    print(request.form)
    # check if email  exists in DB
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Credentials")
        return redirect("/")
    # check to see of the password provided matches the password in our DB
    password_valid = bcrypt.check_password_hash(user.password, request.form['password'])
    print(password_valid)
    if not password_valid:
        flash("Invalid Credentials")
        return redirect('/')
    
    session['user_id'] = user.id
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name
    
    return redirect('/recipes')
    




## logout user and clear session information
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
