from flask import render_template, url_for, flash, redirect, request
from CircuitsTimes import app, db, bcrypt
from CircuitsTimes.forms import RegistrationForm, LoginForm, UpdateAccountForm, AddTimeForm
from CircuitsTimes.models import Users, LapTimes, vehicletype, Tracks, Cars
from flask_login import login_user, current_user, logout_user, login_required
import pandas as pd
import os
import secrets


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/tracks')
@login_required
def tracks():
    track = Tracks.query.all()
    return render_template('tracks.html', value=track)


@app.route('/cars')
@login_required
def cars():
    car = Cars.query.all()
    return render_template('cars.html', value=car)


@app.route('/laptimes')
@login_required
def laptimes():
    conn = db.engine
    laptime = pd.read_sql_query('''SELECT L.*, T.*, C.*, U.* FROM LapTimes L JOIN Cars C ON L.car_id=C.id JOIN Tracks 
    T ON L.track_id=T.id JOIN Users U ON L.user_id=U.id WHERE U.private=0''', conn)
    laptime_small = laptime[['Name', 'Length', 'Time', 'comment', 'username', 'YearOfBirth', 'Make', 'Model',
                             'Power', 'CarSize']]
    return render_template('laptimes.html', tables=[laptime_small.to_html(classes='data', index=False)],
                           titles=laptime_small.columns.values)


@app.route('/mylaptimes')
@login_required
def mylaptimes():
    conn = db.engine
    laptime = pd.read_sql_query('''SELECT L.*, T.*, C.*, U.* FROM LapTimes L JOIN Cars C ON L.car_id=C.id JOIN Tracks 
    T ON L.track_id=T.id JOIN Users U ON L.user_id=U.id WHERE U.id=:yourID''', conn,
                                params={"yourID": current_user.id})
    laptime_small = laptime[['Name', 'date_added', 'Length', 'Time', 'comment', 'username', 'YearOfBirth', 'Make',
                             'Model', 'Power', 'CarSize']]
    laptime_small['Avg Speed'] = laptime_small['Length']/laptime_small['Time']*3600
    laptime_small['Avg Speed'] = laptime_small['Avg Speed'].round(2)
    laptime_small['Avg Speed'] = laptime_small['Avg Speed'].astype(str) + ' km/h'
    laptime_small.columns = ['Track', 'Date of Lap', 'Length', 'Time', 'comment', 'Username', 'Year of birth', 'Make',
                             'Model', 'Power', 'Car Size', 'Avg Speed']
    return render_template('mylaptimes.html', tables=[laptime_small.to_html(classes='data', index=False)],
                           titles=laptime_small.columns.values)


@app.route('/bestlaps')
@login_required
def bestlaps():
    conn = db.engine
    laptime = pd.read_sql_query('''SELECT * FROM (SELECT * FROM (SELECT L.*, T.*, C.*, U.* \
    FROM LapTimes L JOIN Cars C ON L.car_id=C.id JOIN Tracks T ON L.track_id=T.id JOIN Users U ON L.user_id=U.id) AS D \
    WHERE ( SELECT COUNT(*) FROM (SELECT L.*, T.*, C.*, U.* FROM LapTimes L JOIN Cars C ON L.car_id=C.id JOIN Tracks 
    T ON L.track_id=T.id JOIN Users U ON L.user_id=U.id) AS DX WHERE DX.Name = D.Name AND \
    DX.Time <= D.Time) <= 3) AS P WHERE P.private=0 ORDER BY P.Name ASC, P.Time ASC''', conn)
    laptime_small = laptime[['Name', 'Time', 'username', 'Make', 'Model']]
    return render_template('bestlaps.html', tables=[laptime_small.to_html(classes='data', index=False)],
                           titles=laptime_small.columns.values)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        password_in_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(username=form.username.data, YearOfBirth=form.YearOfBirth.data,
                     email=form.email.data, password=password_in_hash)
        db.session.add(user)
        db.session.commit()
        flash('Your LapNote account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.context_processor
def inject_variables():
    if current_user.is_authenticated:
        return dict(user={'name': current_user.username})
    else:
        return dict(user={'name': 'Anonymous'})


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.private = form.private.data
        current_user.CarID = form.CarID.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.private.data = current_user.private
        form.CarID.data = current_user.CarID
    return render_template('account.html', title='Account',
                           form=form)


@app.route("/newtime", methods=['GET', 'POST'])
@login_required
def newtime():
    form = AddTimeForm()
    if form.validate_on_submit():
        lap = LapTimes(comment=form.comment.data, Time=form.time.data, track_id=form.track.data,
                       car_id=form.car.data, user_id=current_user.id)
        db.session.add(lap)
        db.session.commit()
        flash('Your time has been added!', 'success')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.track.data = None
        form.car.data = current_user.CarID
        form.comment.data = None
        form.time.data = None
        current_user.id = None
    return render_template('newtime.html', title='Add new time',
                           form=form)
