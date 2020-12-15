"""
    A bunch of classes to configure our app.
    The main goal to this classes is to provide initial configuration values for our app
    We will have 3 possible environments: production, development, testing.
        1. We will configure a main config class --> class Config
        2. And then, 3 more classes that will inherit from (class Config) and override some of the settings
"""
import logging
import os
# TODO put envs (FLASK_ENV , ect..)
# from dotenv import load_dotenv
# basedir = os.path.abspath(os.path.dirname(__file__))
# load_dotenv(os.path.join(basedir, '.env'))

from os import urandom
# GET THE BASE DIRECTORY FOR THE APP
basedir = os.path.abspath(os.path.dirname(__file__))
print("OUTPUT - basedir: ", basedir)


class Config(object):
    """
    This class has the default configuration for our app
    So, we may consider this one to be THE PRODUCTION CONFIGURATION FILE because( production  will be almost empty ),
    although the existence of ProductionConfig class just below.

    For the DevelopmentConfig and TestingConfig we will override some of the settings present here. Not all...
    """
    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # TODO 1:
    #  1. SHOULD CONSIDER TO SETUP THIS ENV VARIABLE VIA SCRIPT.
    #  2. And/Or try to use encrypt/decrypt functions and store the env in file ?
    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        key = urandom(48) # get a key
        SECRET_KEY= key

    # TODO 2:
    #  We should consider using the below variables as application variables.
    #     # NETWORK DEVICE CREDENTIALS FOR DEVICE CONNECTIVITY - CHECK A BETTER WAY TO STORE THIS VALUES
    #     USER_NAME = "cisco"
    #     USER_PASS = "cisco"
    #     PASSWORD = "password"  # ENTER ON "Privileged EXEC" MODE ON CISCO NETWORK DEVICES.
    #  The class "Connect to Device" and function "guess_device" in file "connect.py" are using this variables.(locally)
    #     they manage the connections to network devices.


    SERVER_NAME = "127.0.0.1:80"  # INTERFACE OR IP WHERE SERVER IS LISTENING FOR REQUESTS. CAN BE --> "0.0.0.0"
    PORT = 80  # SERVER'S PORT LISTENING
    # DON'T ACTIVATE (DEBUG=TRUE) ON PRODUCTION ENV, UNLESS WE WANT TO DEACTIVATE THE FUNCTIONALITY OF SENDING
    # EMAILS TO ADMINS IN CASE OF SERVER INTERNAL ERRORS. ERROR WILL BE ONLY LOGGED ON FILE
    DEBUG = False
    # CONFIGURING DEFAULT FOR LOG VARIABLES
    LOG_NAME = "NetworkAutomateVER20200603"  # log's name
    LOG_FILE = "NetworkAutomate.log"  # log's file name
    JSON_LOG_FILE = "NETWORKAUTOMATE_JSONLOG.json"  # OUR JSON LOG FILE NAME
    NUMBER_OF_BACKUP_FILES_TO_STORE = 10
    MAX_SIZE = 20000000  # The size of rotating files to store (20000000 = 20 MB)
    LOG_LEVEL = logging.INFO  # level for our log check function "setup_logger" docstring for details.
    LOG_FOLDER = "LOGS"  # default folder to store app logs. --> Change it,  to store logs elsewhere. Didn 't  tested on
    #                    # network locations
    # CHECK IF DIRECTORY for log EXISTS, and if not, create it
    if os.path.exists(LOG_FOLDER) is False:
        print("Make directory: ", LOG_FOLDER)  # WE ARE ASSUMING THAT WE HAVE PRIVILEGES FOR WRITE IN THE APP FOLDER.
        os.mkdir(LOG_FOLDER)



    # SWAGGER SPECIFIC VALUES -Settings for our documentation api
    SWAGGER_URL = '/documentation'  # this is endpoint url to our documentation. We can change to e.g. '/api_docs'
    API_URL = '/static/documentation.yaml'  # file with specifications openAPI 2.0 - could be json if we want.

    # SETUP CONFIGURATION SO THAT OUR SERVER APP COULD SEND AN EMAIL TO A LIST OF ADMINS IN CASE OF SERVER ERROR
    # THIS VALUES AND VARIABLES FOR MAIL CONFIG,  WILL ONLY BE USED IN A PRODUCTION ENVIRONMENT
    # (NOT IN development or testing ENVIRONMENT)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None # WHAT IT MEANS
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # GROUP OF EMAILS THAT WILL RECEIVE ERROR MESSAGES WHEN APPLICATION FAILS. and Email is configured on server
    #ADMINS = ["your_admin_email_account@domain.com"]  # Add, Delete or Edit the list of emails.
    ADMINS = ["nuno.moura10000@outlook.pt"]  # Add, Delete or Edit the list of emails. We do not test we the list Empty.

    # CISCO DEVICE CREDENCIALS:
    DEVICE_USERNAME = "cisco"
    DEVICE_PASSWORD = "cisco"
    DEVICE_SECRET = "password" # for entering on exec mode (equivalent of doing a "enable" command in cisco CLI)

    # FOR COOKIES, SESSIONS, HTTPS, please CHECK THIS SOURCE:
    # since we are not managing client sessions and cookies the app is configured with FLASK default´s
    # https://flask.palletsprojects.com/en/1.1.x/security/#security-cookie



class ProductionConfig(Config):
    """
    This class will inherit all the properties from the parent class 'Config'
    All the settings are configured in the parent class.
    """
    CONFIG_NAME = "production"  # name for config
    pass


class DevelopmentConfig(Config):
    """
    This class will inherit from the Config class, and will override some of the settings
    It will be used While on Debug mode
    """

    DEBUG = True  # WE WANT THIS MODE TRUE on development env
    CONFIG_NAME = "development"  # name for config
    # OVERRIDE LOG LEVEL
    LOG_LEVEL = logging.DEBUG  # level for our log check function "setup_logger" docstring for details.
    # CONFIGURING DEFAULT LOG VARIABLES AND VALUES For --> development environment
    LOG_NAME = "NetworkAutomateVER20200603"  # log's name
    LOG_FILE = "NetworkAutomate.log"  # log's file name
    NUMBER_OF_BACKUP_FILES_TO_STORE = 10
    MAX_SIZE = 20000000  # The size of rotating files to store (20000000 = 20 MB)



    # # Enable testing mode
    # Exceptions are propagated rather than handled by the the the_app’s error handlers.
    # Extensions may also change their behavior to facilitate easier testing. You should enable this in your own tests.
    TESTING = True
    SESSION_COOKIE_SECURE = False

    # #  We should to consider in activating NETMIKO on debug. Check "__init__.py" file for more details.
    # NETMIKO_LOG_FILE_NAME = "NETMIKO_OUTPUT.log"   IT IS NOT PROPERLY CONFIGURED YET,so not decomment this line)


class TestingConfig(Config):
    """
    This class will inherit from the Config class, and will override some of the settings
    It will be used While on testing mode: --> unittesting <--
    """
    CONFIG_NAME = "testing"  # name for config
    # OVERRIDE LOG LEVEL from INFO to DEBUG
    LOG_LEVEL = logging.DEBUG  # level for our log check function "setup_logger" docstring for details.

    # Enable testing mode.
    # Exceptions are propagated rather than handled by the the the_app’s error handlers.
    # Extensions may also change their behavior to facilitate easier testing. You should enable this in your own tests.
    TESTING = True

    # PROPAGATE_EXCEPTIONS
    # Exceptions are re-raised rather than being handled by the the_app’s error handlers.
    # If not set, this is implicitly true if TESTING or DEBUG is enabled.
    # Default: None
    # PRESERVE_CONTEXT_ON_EXCEPTION
    # Don’t pop the request context when an exception occurs. If not set, this is true if DEBUG is true.
    # This allows debuggers to introspect the request data on errors, and should normally not need to be set directly.
    #
    # Default: None
    #
    # TRAP_HTTP_EXCEPTIONS
    # If there is no handler for an HTTPException-type exception, re-raise it to be handled by the interactive debugger
    # instead of returning it as a simple error response.
    #
    # Default: False
    #
    # TRAP_BAD_REQUEST_ERRORS
    # Trying to access a key that doesn't exist from request dicts like args and form will return a 400 Bad Request
    # error page. Enable this to treat the error as an unhandled exception instead so that you get the interactive
    # debugger.
    # This is a more specific version of TRAP_HTTP_EXCEPTIONS. If unset, it is enabled in debug mode.
    #
    # Default: None
    SESSION_COOKIE_SECURE = False
