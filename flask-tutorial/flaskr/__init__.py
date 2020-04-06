import os

from flask import Flask


def create_app(test_config=None):

    # Create and configure the app #
    # instance_relative_config = True tells the app that configuration files are relative to the instance folder
    # the instance folder is located outside the flaskr package and can hold local data that shouldn't be
    # committed to version control, such as configuration secrets and the database file.
    application = Flask(__name__, instance_relative_config=True)
    # sets some default configuration hat the app will use:
    application.config.from_mapping(
        # SECRET_KEY is used by Flask extension to keep data safe. It's set to 'dev' to provide a convenient value
        # during development, but it should be overridden with a random value when deploying.
        SECRET_KEY='dev',
        # Database is the path where the SQLite database file will be saved. It's under app.instance_path,
        # which is the path that Flask has chosen for the instance folder
        DATABASE=os.path.join(application.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        application.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        application.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        # os.makedirs() ensures that app.instance_path exists. Flask doesn’t create the instance folder automatically,
        # but it needs to be created because your project will create the SQLite database file there.
        os.makedirs(application.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(application)

    # a simple page that say hello
    @application.route('/hello')
    def hello():
        return 'Hello World!'

    return application
