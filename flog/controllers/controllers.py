from flog import app
from flask import render_template, request, session, url_for, redirect, flash
from ..models import init_db, get_db, check_db

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or \
        request.form['password'] != app.config['PASSWORD']:
            error = 'Incorrect login and/or password!'
        else:
            session['logged_in'] = True
            flash('You were logged in!')
            return redirect(url_for('show_posts'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out!')
    return redirect(url_for('show_posts'))

@app.route('/')
def show_posts():
    check_db()
    db = get_db()
    cur = db.execute('SELECT title, text FROM posts ORDER BY id DESC')
    posts = cur.fetchall()
    return render_template('show_posts.html', posts=posts)

@app.route('/add', methods=['POST'])
def add_post():
    if not session.get('logged_in'):
        flash('You must login!')
        return redirect(url_for('show_posts'))
    db = get_db()
    if request.form['title'] == "" and request.form['text'] == "":
        flash('Fill the data!')
        return redirect(url_for('show_posts'))
    db.execute('INSERT INTO posts (title, text) VALUES (?, ?)',[request.form['title'], request.form['text']])
    db.commit()
    flash('New post was successfully posted')
    return redirect(url_for('show_posts'))