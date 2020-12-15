"""
THIS IS OUR INIT FILE: IT WILL LOAD THE CONFIGs TO OUR APP
"""
from config import DevelopmentConfig, ProductionConfig, TestingConfig, Config
import logging
from logging.handlers import SMTPHandler
from .teste_backup_operations import setup_logger
import os
from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask
from the_app.routes import api
from werkzeug.exceptions import HTTPException
from the_app.routes import internal_server_error, handle_exception,  handle_invalid_usage
from the_app.request_data import InvalidUsage


__title__ = 'NETWORKAUTOMATE'
__version__ = 'Development.2020'
__author__ = 'Nuno Moura'
__email__ = 'nm.10000.testes@gmail.com'
__license__ = 'free to use'
__copyright__ = 'None'


def create_app(config_class=None):
    """
    FLASK PATTERN FACTORY - this function will create our app
    :return:
    """
    # CREATING INSTANCE OF FLASK OBJECT NAMED "app"
    app = Flask(__name__)

    if config_class is None:
        config_class = ProductionConfig
        if os.environ.get('FLASK_ENV') == "production":
            config_class = ProductionConfig
        elif os.environ.get('FLASK_ENV') == "testing":
            # app.config.from_object(TestingConfig)
            config_class = TestingConfig
        else:
            config_class = DevelopmentConfig
            # app.config.from_object(DevelopmentConfig)
    else:
        # config_class value is passed directly to the function create_app()
        pass

    # CONFIGURE THE APP FROM  object (there are some classes in "config.py")
    app.config.from_object(config_class)

    print("OUTPUT - FLASK_ENV: " + str(os.environ.get('FLASK_ENV')))
    print('OUTPUT - app.config["ENV"]', app.config["ENV"])

    # ---- CHANGE FLASK DEFAULT LOG SYSTEM -------------------
    # First, check IF FOLDER FOR LOGS EXIST, if not, create it!
    # WE ARE NOT CHECKING FOR PERMISSIONS TO WRITE ON FOLDER.
    # We are expecting to have permissions to write on the_app folder
    FINAL_LOG_PATH_AND_NAME = app.config["LOG_FOLDER"] + "/" + app.config["LOG_FILE"]
    print("="*79)
    # CREATE A LOGGER OBJECT TO LOG TO FILE ---- WE CAN USE THIS logger_engine OBJECT WHENEVER WE WANT IN THE APP
    # Simple USAGE: app.logger.info("message to log") or app.logger.debug("message to log") or
    # app.logger.error("message to log").
    # Since we are going to use flask factory pattern, to use log in other files do:
    # from flask import current_app
    # current_app.logger.info("message") or current_app.logger.error("message").
    app.logger = setup_logger(name=app.config["LOG_NAME"],
                              log_file_name=FINAL_LOG_PATH_AND_NAME,
                              max_size=app.config["MAX_SIZE"],
                              level=app.config["LOG_LEVEL"],
                              number_of_backup_files_to_store=app.config["NUMBER_OF_BACKUP_FILES_TO_STORE"])

    # -- ------ --FOR NETMIKO DEBUG LOG ---------
    # Check, how to create a handler and add this new handler to existing log. (app.logger). We only need Netmiko log
    # WHILE our app is on DEBUG mode. (For troubleshoot connections debugging)
    # logger1 = logging.getLogger("netmiko")

    # WRITE ON THE LOG THAT OUR APP IS STARTING
    app.logger.warning("OUTPUT: STARTING THE FLASK APP SERVER")
    app.logger.warning("OUTPUT: SERVING THE APP in 'mode': {}".format(app.config["ENV"]))
    app.logger.warning("OUTPUT: app.config['DEBUG']: {}".format(app.config["DEBUG"]))
    app.logger.debug("OUTPUT: FINAL_LOG_PATH_AND_NAME:  " + str(FINAL_LOG_PATH_AND_NAME))
    app.logger.debug("OUTPUT: app.config: {}".format(app.config))

    # START DOING CONFIG ON SWAGGER. OUR Documentation Api
    app.logger.debug("OUTPUT: SWAGGER_URL {}".format(app.config["SWAGGER_URL"]))
    app.logger.debug("OUTPUT: SWAGGER --> API_URL: {}".format(app.config["API_URL"]))
    swaggerui_blueprint = get_swaggerui_blueprint(
        app.config["SWAGGER_URL"],  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
        app.config["API_URL"],  # file with specifications (this settings are in the config.py)
        # in config classes
        config={  # Swagger UI config overrides
            'app_name': "NETWORK_AUTOMATE"
        },
        # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
        #    'clientId': "your-client-id",
        #    'clientSecret': "your-client-secret-if-required",
        #    'realm': "your-realms",
        #    'appName': "your-app-name",
        #    'scopeSeparator': " ",
        #    'additionalQueryStringParams': {'test': "hello"}
        # }
    )
    # Register blueprint at URL
    # (URL must match the one given to factory function above)
    app.register_blueprint(swaggerui_blueprint, url_prefix=app.config["SWAGGER_URL"])



    # REGISTER ERRORS
    # Flask doesnt support blueprint level error handlers for 404 and 500 errors.
    # error_handler(code_or_exception)
    # Registers an error handler that becomes active for this blueprint only. Please be aware that routing does not
    # happen local to a blueprint so an error handler for 404 usually is not handled by a blueprint unless it is caused
    # inside a view function. Another special case is the 500 internal server error which is always looked up m
    # the application.

    # Register the "api blueprint" in flask app. "api" have all the existing routes except the routes for documentation.
    app.register_blueprint(api)


    #app.register_error_handler(HTTPException, handle_exception)
    app.register_error_handler(Exception, internal_server_error)
    #print(app.register_error_handler)

    # Comment this on production or log to file on debug mode....
    # print("OUTPUT - app.name: {}".format(app.name))
    # print("OUTPUT - app.url_map: {}".format(app.url_map))
    # print("OUTPUT - app.template_folder: ", app.template_folder)
    # print("OUTPUT - app.blueprints: ", app.blueprints)

    # WE only go to enable the email logger when the application is running without debug mode,
    # which is indicated by the_app.debug being True, and also when the email server exists in the configuration.
    # Setting up the email logger is somewhat tedious due to having to handle optional security options that are present
    # in many email servers. But in essence, the code above creates a SMTPHandler instance, sets its level so that it
    # only reports errors and not warnings, informational or debugging messages, and finally attaches it
    # to the the_app.logger object from Flask.
    if not app.debug:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject=app.name + " Failure",
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
    return app
