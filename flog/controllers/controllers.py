from flask import render_template, request, session, url_for, redirect, flash
from flask.views import MethodView
from flog.models import get_from_db, add_to_db, save_file_datetime, check_login, posts_page


def login():
    """
    Login
    """
    error, code = None, None
    if request.method == 'POST':
        if not check_login(request.form['username'], request.form['password']):
            error = 'Incorrect login and/or password!'
            code = 401
        else:
            session['logged_in'] = True
            flash('You were logged in!')
            return redirect(url_for('show_posts'))
    return render_template('login.html', error=error), code


def logout():
    """
    Logout
    """
    session.pop('logged_in', None)
    flash('You were logged out!')
    return redirect(url_for('show_posts'))


def show_posts():
    """
    Show the posts with limit of pagination
    """
    page = request.args.get('page', type=int, default=1)
    posts = get_from_db()
    pagination, posts = posts_page(page, posts)
    return render_template(
        'show_posts.html', posts=posts, pagination=pagination)


def add_post():
    """
    Add the post
    """
    filename, filesave, date_time, title, text = None, None, None, '', ''
    if not session.get('logged_in'):
        flash('You must login!')
        return redirect(url_for('show_posts'))
    title, text = request.form['title'], request.form['text']
    if title == "" and text == "":
        flash('Fill the data!')
        return redirect(url_for('show_posts'))
    files = request.files['filename']
    if not files.filename == "":
        filename, filesave, date_time = save_file_datetime(files)
        if filename:
            pass
        else:
            flash('Please, choose: mp3 / jpg / jpeg / gif / png!')
            filename = None
    add_to_db(date_time, title, text, filename, filesave)
    flash('New post was successfully posted')
    return redirect(url_for('show_posts'))
