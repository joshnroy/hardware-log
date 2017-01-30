from flask import Flask
from flask_pymongo import PyMongo
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
mongo = PyMongo(app)
from flask import render_template, flash, redirect, request
from app import app, lm
from .forms import AddForm, RentForm, LoginForm
from .user import User
from flask.ext.login import login_user, logout_user, login_required
from uuid import uuid4

@app.route('/')
@app.route('/index')
def index():
    available = {}
    for x in mongo.db.hardware.find({'status': 'available'}):
        if x['name'] in available.keys():
            available[x['name']] += 1
        else:
            available[x['name']] = 1
    rented = mongo.db.hardware.find({'status': 'rented'})
    requested = mongo.db.hardware.find({'status': 'requested'})
    return render_template('index.html', available=available, rented=rented,
            requested=requested)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = AddForm()
    if form.validate_on_submit():
        for i in range(form.number.data):
            mongo.db.hardware.insert_one({'name': form.name.data,
                'renter-name': '', 'renter-email': '',
                'renter-phone-number': '', 'status': 'available', 'uuid':
                uuid4().hex})
        return redirect('/index')
    return render_template('add.html', form=form)

@app.route('/rent', methods=['GET', 'POST'])
def rent():
    form = RentForm()
    form.name.choices = {(x['name'], x['name']) for x in
            mongo.db.hardware.find({'status': 'available'})}
    if form.validate_on_submit():
        for x in form.name.data:
            mongo.db.hardware.update_one({'name': x, 'status':
                'available'}, 
                {
                    '$set': {'renter-name': form.renter_name.data, 'renter-email':
                        form.renter_email.data, 'renter-phone-number':
                        form.renter_phone_number.data, 'status': 'requested',
                        'renter-idea': form.renter_idea.data}})
        return redirect('/index')
    return render_template('rent.html', form=form)

@app.route('/confirm')
@login_required
def confirm():
    id = request.args.get('uuid')
    mongo.db.hardware.update_one({'uuid': id}, {'$set': {'status': 'rented'}})
    return redirect('/index')

@app.route('/return')
@login_required
def unrent():
    id = request.args.get('uuid')
    mongo.db.hardware.update_one({'uuid': id}, {'$set': {'renter-name':
        '', 'renter-email': '', 'renter-phone-number': '', 'status':
        'available'}})
    return redirect('/index')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = app.config['USERS_COLLECTION'].find_one({"_id": form.username.data})
        if user and User.validate_login(user['password'], form.password.data):
            user_obj = User(user['_id'])
            login_user(user_obj)
            flash("Logged in successfully!", category='success')
            return redirect(request.args.get("next") or '/index')
        flash("Wrong username or password!", category='error')
    return render_template('login.html', title='login', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@lm.user_loader
def load_user(username):
    u = app.config['USERS_COLLECTION'].find_one({"_id": username})
    if not u:
        return None
    return User(u['_id'])
