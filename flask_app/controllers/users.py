# controller.py
from flask_bcrypt import Bcrypt
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User

bcrypt = Bcrypt(app)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        # we redirect to the template with the form.
        return redirect('/')
    # ... do other things
    hashword = bcrypt.generate_password_hash(request.form["password"])
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": hashword
    }

    User.save(data)
    session['name'] = request.form['first_name']
    return redirect('/dashboard')



@app.route('/login',methods=['post'])
def login():

    data = {
        'email': request.form['email']
    }
    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash("Invalid email/password",'login')
        return redirect('/')

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid email/password", 'login')
        return redirect('/')

    
    session['name'] = user_in_db.first_name

    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    print(session)
    if not session:
        return redirect('/')

    
    return render_template('dashboard.html', name = session)


@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')