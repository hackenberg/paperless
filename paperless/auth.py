import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from paperless.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        query = 'SELECT * FROM account WHERE id = ?'
        params = (user_id,)
        g.user = get_db().execute(query, params).fetchone()


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            query = 'SELECT id FROM account WHERE username = ?'
            params = (username,)
            if db.execute(query, params).fetchone() is not None:
                error = f'User {username} is already registered.'

        if error is None:
            query = 'INSERT INTO account (username, password) VALUES (?, ?)'
            params = (username, generate_password_hash(password))
            db.execute(query, params)
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            query = 'SELECT * FROM account WHERE username = ?'
            params = (username,)
            user = db.execute(query, params).fetchone()

        if user is None or not check_password_hash(user['password'], password):
            error = 'Authentication failure.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('docs.index'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
