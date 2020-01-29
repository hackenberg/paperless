from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort

from paperless.auth import login_required
from paperless.db import get_db

bp = Blueprint('docs', __name__, url_prefix='/docs')


@bp.route('/')
def index():
    query = '''
        SELECT d.id, title, content, created, account_id, username
        FROM document d JOIN account a ON d.account_id = a.id
        ORDER BY created DESC
        '''
    docs = get_db().execute(query).fetchall()
    return render_template('docs/index.html', docs=docs)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            query = '''
                INSERT INTO document (title, content, account_id)
                VALUES (?, ?, ?)
                '''
            params = (title, content, g.user['id'])
            db.execute(query, params)
            db.commit()
            return redirect(url_for('docs.index'))

    return render_template('docs/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    doc = get_doc(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            query = 'UPDATE document SET title = ?, content = ? WHERE id = ?'
            params = (title, content, id)
            db.execute(query, params)
            db.commit()
            return redirect(url_for('docs.index'))

    return render_template('docs/update.html', doc=doc)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_doc(id)
    db = get_db()
    query = 'DELETE FROM document WHERE id = ?'
    params = (id,)
    db.execute(query, params)
    db.commit()
    return redirect(url_for('docs.index'))


def get_doc(id, check_author=True):
    query = '''
        SELECT d.id, title, content, created, account_id, username
        FROM document d JOIN account a on d.account_id = a.id
        WHERE d.id = ?
        '''
    params = (id,)
    doc = get_db().execute(query, params).fetchone()

    if doc is None:
        abort(404, f'Document id {id} does not exist.')

    if check_author and doc['account_id'] != g.user['id']:
        abort(403)

    return doc
