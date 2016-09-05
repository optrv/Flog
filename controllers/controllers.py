from flog import app
from flask import render_template, request, session, url_for, redirect, flash
from flog.models import get_from_db, add_to_db
from werkzeug.utils import secure_filename
import os

@app.route('/login', methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if (request.form['username'] != app.config['USERNAME'] or
        request.form['password'] != app.config['PASSWORD']):
            error = 'Incorrect login and/or password!'
        else:
            session['logged_in'] = True
            flash('You were logged in!')
            return redirect(url_for('show_posts'))
    return render_template('login.html', error = error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out!')
    return redirect(url_for('show_posts'))

@app.route('/')
def show_posts():
    return render_template('show_posts.html', posts = get_from_db())

@app.route('/add', methods = ['POST'])
def add_post():
    if not session.get('logged_in'):
        flash('You must login!')
        return redirect(url_for('show_posts'))
    if request.form['title'] == "" and request.form['text'] == "":
        flash('Fill the data!')
        return redirect(url_for('show_posts'))
    files = request.files['file']
    if not files.filename == "":
        if files.filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']:
            filename = secure_filename(files.filename)
            if filename.rsplit('.', 1)[1] != 'mp3':
                subfolder = 'image/'
            else:
                subfolder = 'music/'
            files.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], subfolder, files.filename))
        else:
            flash('Please, choose: mp3 / jpg / jpeg / gif / png!')
            files.filename = None
    add_to_db(request.form['title'], request.form['text'], files.filename)
    flash('New post was successfully posted')
    return redirect(url_for('show_posts'))