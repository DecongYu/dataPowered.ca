import os
from flask import Flask

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='#dev-need\\to\\change',
        DATABASE=os.path.join(app.instance_path, 'shale.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # register the init_app
    from . import db
    db.init_app(app)

    # register auth blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    from . import wells
    app.register_blueprint(wells.bp)
    app.add_url_rule('/', endpoint='index')


    return app
