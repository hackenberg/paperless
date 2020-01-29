import os

from flask import Flask, escape, request


def create_app(test_config=None):
    '''Application Factory'''
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'dev.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config
        app.config.from_mapping(test_config)

    try:
        # ensure the instance folder exists
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    @app.route('/')
    def index():
        name = request.args.get('name', 'World')
        return f'Hello, {escape(name)}!'

    return app
