import os

from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from api.route.home import home_api, map
from argparse import ArgumentParser


def create_app():
    """
    Create a Flask application with its Swagger documentation.

    Returns
    -------
    Flask
        Flask application
    """
    app = Flask(__name__, template_folder=os.path.join('api', 'templates'), static_folder=os.path.join('api'))
    CORS(app)

    app.config['SWAGGER'] = {
        'title': 'API madridalfresco Documentation',
    }
    Swagger(app)
    app.register_blueprint(home_api, url_prefix='/api')
    app.register_blueprint(map, url_prefix='/')

    return app


if __name__ == '__main__':
    # Configuration of the API
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args, unknown = parser.parse_known_args()
    port = args.port

    # Creating documentation and configure API paths
    application = create_app()

    # Running the api
    application.run(host='0.0.0.0', port=port)
