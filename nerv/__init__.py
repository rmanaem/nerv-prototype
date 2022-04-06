from flask import Flask


def create_app(path):
    """Construct core Flask application with embedded Dash app."""
    app = Flask(__name__)
    # app = Flask(__name__, instance_relative_config=False)
    # app.config.from_object('config.Config')

    with app.app_context():
        # Import Flask routes
        from nerv import routes

        # Import Dash application
        from nerv.app import create_dashboard
        app = create_dashboard(app, path)

        return app
