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
    if request.method == 'GET':
        return render_template('register.html')
    
    if request.method == 'POST':
        username = request.form.get('username',None)
        email = request.form.get('email',None)
        password = request.form.get('password',None)
        cpassword = request.form.get('cpassword',None)
        role = request.form.get('role',None)
        image = request.files.get('image',None)

        # addresss = request.form.get('address',None)
        # phone = request.form.get('phone',None)

        # relationship
        # cust = Customer(address= addresss,
        #             phone = phone)
        
        # user = User(username=username,
        #             email=email,
        #             password=password,
        #             customer_dets = cust)
        
        # db.session.add(user)
        # db.session.commit()

        #without relationship

        # user = User(username=username,
        #             email=email,
        #             password=password,
        #             roles = [Role.query.filter_by(name=role).first()])
        # db.session.add(user)
        # user = User.query.filter_by(username=username).first()
        # cust = Customer(address= addresss,
        #                 phone = phone,
        #                 user_id = user.id)
        # db.session.add(cust)
        # db.session.commit()


        # Data Validation
        if not username:
            flash('Username is required')
            return redirect(url_for('register'))
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists')
            return redirect(url_for('login'))
        
        if not email:
            flash('Email is required')
            return redirect(url_for('register'))
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists')
            return redirect(url_for('login'))
        
        if not password and not cpassword:
            flash('Password is required')
            return redirect(url_for('register'))
        
        if password != cpassword:
            flash('Password and Confirm Password must be same')
            return redirect(url_for('register'))
        
        if not role:
            flash('Role is required')
            return redirect(url_for('register'))
        
        image_file_path = None
        if image:
            image_file_path = 'images/' + image.filename
            absoulte_path = 'static/' + image_file_path
            image.save(absoulte_path)

        # url_for('static', filename=image_file_path)

        approved = True
        if role == 'store_manager':
            approved = False

        user = User(username = username,
                    email = email,
                    password = password,
                    image_file = image_file_path,
                    approved = approved,
                    roles = [Role.query.filter_by(name=role).first()])
        db.session.add(user)
        db.session.commit()
        flash('User created successfully')
        return redirect(url_for('login'))

@app.route('/user_approvals')
def user_approvals():
    approved_users = User.query.filter_by(approved=True).all()
    approved_store_managers = []
    customers = []
    for user in  approved_users:
        if 'store_manager' in [role.name for role in user.roles]:
            approved_store_managers.append(user)
        if 'customer' in [role.name for role in user.roles]:
            customers.append(user)

    approval_requests = User.query.filter_by(approved=False).all()
    return render_template('all_user_details.html', 
                           approved_store_managers=approved_store_managers,
                           customers=customers, 
                           approval_requests=approval_requests)


# /approve_user/1
# /approve_user/2
@app.route('/approve_user/<int:user_id>')
def approve_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    # user = User.query.get(user_id)  -- when querying by primary key
    if not user:
        flash('User not found')
        return redirect(url_for('user_approvals'))
    
    user.approved = True
    db.session.commit()
    flash('User approved successfully')
    return redirect(url_for('user_approvals'))

# @app.route('/reject_user/<int:user_id>/user/<string:role>') -- multiple parameters possible
@app.route('/reject_user/<int:user_id>')
def reject_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        flash('User not found')
        return redirect(url_for('user_approvals'))
    
    db.session.delete(user)
    db.session.commit()

# @app.route('/delete_user/<int:user_id>')
# def delete_user(user_id):
#     user = User.query.filter_by(id=user_id).first()
#     if not user:
#         flash('User not found')
#         return redirect(url_for('user_approvals'))
    
#     db.session.delete(user)
#     db.session.commit()

#     flash('User rejected successfully')
#     return redirect(url_for('user_approvals'))

@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if request.method == 'GET':
        return render_template('add_category.html')
    
    if request.method == 'POST':
        category_name = request.form.get('category_name', None)
        description = request.form.get('description', None)

        # Data Validation
        if not category_name:
            flash('Category Name is required')
            return redirect(url_for('add_category'))
        
        category = Categories.query.filter_by(name=category_name).first()
        if category:
            flash('Category already exists')
            return redirect(url_for('add_category'))
        
        if not description:
            flash('Description is required')
            return redirect(url_for('add_category'))
        
        try: 
            category = Categories(name=category_name, 
                                  description=description)
            db.session.add(category)
            db.session.commit()
            flash('Category added successfully')
            return redirect(url_for('add_category'))
        except Exception as e:
            # db.session.rollback()
            flash(f'Error while adding category: {e}')
            return redirect(url_for('add_category'))
    
@app.route('/view_categories')
def view_categories():
    categories = Categories.query.all()
    return render_template('categoryView.html', categories=categories)

@app.route('/edit_category/<int:category_id>', methods=['POST'])
def edit_category(category_id):
    category = Categories.query.filter_by(id=category_id).first()
    if not category:
        flash('Category not found')
        return redirect(url_for('view_categories'))
    
    new_category_name = request.form.get('category_name', None)
    new_description = request.form.get('description', None)

    # Data Validation
    cat_check = Categories.query.filter_by(name=new_category_name).first()
    if cat_check:
        flash('Category already exists')
        return redirect(url_for('view_categories'))
    
    if new_category_name:
        category.name = new_category_name

    if new_description:
        category.description = new_description

    db.session.commit()
    flash('Category updated successfully')
    return redirect(url_for('view_categories'))
                    
        

            






        
