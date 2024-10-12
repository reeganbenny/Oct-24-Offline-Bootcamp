from main import app
from flask import render_template, session, url_for, redirect, request ,flash
from applications.model import *

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get('email', None)
        password = request.form.get('password', None)

        # Data Validation
        if not email:
            flash('Email is required')
            return redirect(url_for('login'))
        if not password:
            flash('Password is required')
            return redirect(url_for('login'))
        
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('Invalid email')
            return redirect(url_for('login'))
        
        # user_role = Role.query.filter_by(name='store_manager').first()
        if  'store_manager' in [role.name for role in user.roles] and not user.approved:
            flash('Your sign up request not approved! Please contact admin')
            return redirect(url_for('login'))
        
        if user.password == password:
            session['username'] = user.username
            session['role'] = [role.name for role in user.roles]
            flash('Login Successfully')
            return redirect(url_for('home'))
        else:
            flash('Invalid password')
            return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('home'))


@app.route('/signup', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


        
