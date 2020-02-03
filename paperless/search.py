from flask import Blueprint, flash, render_template, request

from paperless.db import get_db

bp = Blueprint('search', __name__, url_prefix='/search')


@bp.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        expression = request.form['search']
        error = None
        if not expression:
            error = 'Expression is required.'

        if not error:
            query = 'SELECT * FROM search WHERE search = ?'
            result = get_db().execute(query, (expression,)).fetchall()
            return render_template('search/index.html', result=result)

        flash(error)

    return render_template('search/index.html', result=[])
