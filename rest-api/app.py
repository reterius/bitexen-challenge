import datetime
import logging

from flasgger import Swagger
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_mongoengine import MongoEngine
from flask_restful import Api

from src.commons.handlers import jwt_handlers_config, response_handlers_config, exception_handlers_config, \
    jsonschema_handlers_config
from src.injects import injects_config
from src.routes import routes_config
from src.utils.dict_util import get_value

# from mongoengine import connect, register_connection

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

app = Flask(__name__)

CORS(app)
jwt = JWTManager(app)
ma = Marshmallow(app)
api = Api(app)


def configure():
    app.config.from_envvar('APP_CONFIG')

    if get_value("LOG_STATUS", app.config, "TERMINAL") == "FILE":
        logging.basicConfig(
            filename=get_value("LOG_FILE_PATH", app.config, "log/transaction_{0}.log").format(
                datetime.datetime.today().date()),
            level=get_value("LOG_LEVEL", app.config, "DEBUG"),
            format=get_value("LOG_FORMAT", app.config),
            datefmt=get_value("LOG_FILE_PATH", app.config)
        )


def migrate():
    pass


def starter():
    sentry_sdk.init(
        dsn=get_value("dsn", get_value("SENTRY", app.config)),
        integrations=[FlaskIntegration()]
    )

    swagger = Swagger(app)

    db = MongoEngine()
    db.init_app(app)

    app.run(
        host=get_value("HOST", app.config, "127.0.0.1"),
        port=get_value("PORT", app.config, 9000),
        debug=get_value("DEBUG", app.config, True)
    )


def main():
    try:
        configure()
        jwt_handlers_config(jwt)
        response_handlers_config(app)
        exception_handlers_config(app)
        jsonschema_handlers_config(app)
        migrate()
        routes_config(api)
        injects_config(app)
        starter()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
