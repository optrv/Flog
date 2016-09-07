from flask import render_template, request, session, url_for, redirect, flash
from flog.models import get_from_db, add_to_db, save_file, check_login

def login():
    error = None
    if request.method == 'POST':
        if not check_login(request.form['username'], request.form['password']):
            error = 'Incorrect login and/or password!'
        else:
            session['logged_in'] = True
            flash('You were logged in!')
            return redirect(url_for('show_posts'))
    return render_template('login.html', error = error)

def logout():
    session.pop('logged_in', None)
    flash('You were logged out!')
    return redirect(url_for('show_posts'))

def show_posts():
    return render_template('show_posts.html', posts = get_from_db())

def add_post():
    if not session.get('logged_in'):
        flash('You must login!')
        return redirect(url_for('show_posts'))
    if request.form['title'] == "" and request.form['text'] == "":
        flash('Fill the data!')
        return redirect(url_for('show_posts'))
    files = request.files['file']
    if not files.filename == "":
        if save_file(files):
            pass
        else:
            flash('Please, choose: mp3 / jpg / jpeg / gif / png!')
            files.filename = None
    add_to_db(request.form['title'], request.form['text'], files.filename)
    flash('New post was successfully posted')
    return redirect(url_for('show_posts'))