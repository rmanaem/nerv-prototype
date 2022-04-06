from flask import Flask, render_template
from nerv.app import start
from nerv.app1 import test


def create_app(path):
    # routes = []

    app = Flask(__name__)
    # app = Flask(__name__, instance_relative_config=False)
    # app.config.from_object('config.Config')

    @app.route('/')
    def home():
        """Landing page."""
        return render_template('index.jinja2',
                               title='Plotly Dash & Flask Tutorial',
                               template='home-template',
                               body="This is a homepage served with Flask.")

    with app.app_context():
        # Import Flask routes
        # from nerv import routes

        # Import Dash application
        # from nerv.app import create_dashboard
        app = start(path, app)

        return app
