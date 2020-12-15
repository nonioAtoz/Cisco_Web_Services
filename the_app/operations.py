from re import compile
import logging
from logging.handlers import RotatingFileHandler
from os import path, mkdir
from flask import request
#from .f_handling_exceptions import DataError  # NOT IN USE


def get_http_request_info(request):
    """
    THIS FUNCTION NOT IN USE.
    THERE  IS A FUNCTION WITH THE SAME NAME IN file 'request_data.py' . its in use

    This function will tell important information about a client that make a request to a Flask  web service
    This may be useful for our logSystem
    read the docs available  for "request" --> flask.request

    FOR BETTER MANAGEMENT OF THE APP MEMORY AND FASTER SPEEDS, WE MUST CONSIDER JUST TO EXPORT ONE DICT FROM,
    THIS FUNCTION BECAUS EWE WILL NOT NEED THE DATA AND IS AVAILABLE FROM --> app.request

    :param request: http request
    :return: <tupple> 2 items
     item 1 <dictionary> flask environment variables of the HTTP request
     item 2 <dictionary> FILTERED/Customized information about client http request ()
    """
    #app.logger.debug("EXECUTING FUNCTION: get_http_request_info")
    # BELOW, WE WILL CATCH A BUNCH OF fLASK ENVIRONMENT VALUES , RELATED TO THE REQUEST . SOME MAY BE USEFUL, OTHER NOT.
    # WE MAY WANT TO REMOVE SOME OF THEM.
    # MEANWHILE ...  WE WILL REGISTER THEM ALL.
    wsgi_version = str(request.environ.get('wsgi.version'))
    wsgi_url_scheme = str(request.environ.get('wsgi.url_scheme'))
    wsgi_multithread = str(request.environ.get('wsgi.multithread'))
    wsgi_multiprocess = str(request.environ.get('wsgi.multiprocess'))
    SERVER_SOFTWARE = str(request.environ.get('SERVER_SOFTWARE'))
    REQUEST_METHOD = str(request.environ.get('REQUEST_METHOD'))
    SCRIPT_NAME = str(request.environ.get('SCRIPT_NAME'))
    PATH_INFO = str(request.environ.get('PATH_INFO'))
    RAW_URI = str(request.environ.get('RAW_URI'))
    REQUEST_URI = str(request.environ.get('REQUEST_URI'))
    REMOTE_ADDR = str(request.environ.get('REMOTE_ADDR'))
    REMOTE_PORT = str(request.environ.get('REMOTE_PORT'))
    SERVER_NAME = str(request.environ.get('SERVER_NAME'))
    SERVER_PORT = str(request.environ.get('SERVER_PORT'))
    SERVER_PROTOCOL = str(request.environ.get('SERVER_PROTOCOL'))
    HTTP_USER_AGENT = str(request.environ.get('HTTP_USER_AGENT'))
    HTTP_CACHE_CONTROL = str(request.environ.get('HTTP_CACHE_CONTROL'))
    HTTP_ACCEPT = str(request.environ.get('HTTP_ACCEPT'))
    HTTP_HOST = str(request.environ.get('HTTP_HOST'))
    HTTP_ACCEPT_ENCODING = str(request.environ.get('HTTP_ACCEPT_ENCODING'))
    CONTENT_LENGTH = str(request.environ.get('CONTENT_LENGTH'))
    HTTP_CONNECTION = str(request.environ.get('HTTP_CONNECTION'))
    werkzeug_request = str(request.environ.get('werkzeug.request'))
    base_url = str(request.base_url)
    request_headers = str(request.headers)

    # BUILD DICTIONARY FOR OUTPUT WITH OUR DATA, and output it
    environment_data = {
        'WSGI_VERSION': wsgi_version,
        'WSGI_URL_SCHEME': wsgi_url_scheme,
        'WSGI_MULTITHREAD': wsgi_multithread,
        'WSGI_MULTIPROCESS': wsgi_multiprocess,
        'SERVER_SOFTWARE': SERVER_SOFTWARE,
        'REQUEST_METHOD': REQUEST_METHOD,
        'SCRIPT_NAME': SCRIPT_NAME,
        'PATH_INFO': PATH_INFO,
        'RAW_URI': RAW_URI,
        'REQUEST_URI': REQUEST_URI,
        'REMOTE_ADDR': REMOTE_ADDR,
        'REMOTE_PORT': REMOTE_PORT,
        'SERVER_NAME': SERVER_NAME,
        'SERVER_PORT': SERVER_PORT,
        'SERVER_PROTOCOL': SERVER_PROTOCOL,
        'HTTP_USER_AGENT': HTTP_USER_AGENT,
        'HTTP_CACHE_CONTROL': HTTP_CACHE_CONTROL,
        'HTP_ACCEPT': HTTP_ACCEPT,
        'HTTP_HOST': HTTP_HOST,
        'HTTP_ACCEPT_ENCODING' :HTTP_ACCEPT_ENCODING,
        'CONTENT_LENGTH' : CONTENT_LENGTH,
        'HTTP_CONNECTION': HTTP_CONNECTION,
        'WERKZEUG_REQUEST': werkzeug_request,
        'BASE_URL': base_url,
        'REQUEST_HEADERS': request_headers}

    network_automate_custom_data= {'REQUEST_METHOD': REQUEST_METHOD,
                                          'REQUEST_URI': REQUEST_URI,
                                          'REMOTE_ADDR': REMOTE_ADDR,
                                          'REMOTE_PORT': REMOTE_PORT,
                                          'HTTP_USER_AGENT': HTTP_USER_AGENT,
                                          'HTTP_CACHE_CONTROL': HTTP_CACHE_CONTROL,
                                          'HTP_ACCEPT': HTTP_ACCEPT,
                                          'HTTP_HOST': HTTP_HOST,
                                          'HTTP_ACCEPT_ENCODING': HTTP_ACCEPT_ENCODING,
                                          'CONTENT_LENGTH': CONTENT_LENGTH,
                                          'HTTP_CONNECTION': HTTP_CONNECTION,
                                          'BASE_URL': base_url,
                                          'REQUEST_HEADERS': request_headers}

    #app.logger.debug( "environment_data: {} \n "
    #                 "network_AutomateAPI_Customized_data {}".format(environment_data, network_automate_custom_data))
    return environment_data, network_automate_custom_data


# THERE IS A function setup_loger in file "request_data.py" with the same name and is not in use
def setup_logger(name, log_file_name, level=None, max_size=None, number_of_backup_files_to_store=None,type =None):
    """
    Creates a rotating log -
    max size of log file is 20 MB
    Store till 10 files, then Rotate

    sources:
        # https://stackoverflow.com/questions/11232230/logging-to-two-files-with-different-settings
        # https://medium.com/@trstringer/logging-flask-and-gunicorn-the-manageable-way-2e6f0b8beb2f

    *IMPORTANT--> WE CAN CHANGE the values from the file VIA config.py
    # Comments:
        # IF WE WANT TO RUN IN DEBUG MODE to log all messages
            # CHANGE level using Formatter ( above ) >>> level=logging.DEBUG
        # IF WE WANTO TO RUN AND LOG JUST IMPORTANT MESSAGES
            # CHANGE level using Formatter ( above ) >>> level=logging.INFO
    --------------------------------------------------------------------------------------------------------------------
    # LOG levels brief Explanation
        DEBUG --> Detailed information, typically of interest only when diagnosing problems.
        INFO --> Confirmation that things are working as expected.
        WARNING --> An indication that something unexpected happened, or indicative of some problem in the near future
         (e.g. ‘disk space low’). The software is still working as expected.
        ERROR -->Due to a more serious problem, the software has not been able to perform some function.
        CRITICAL --> A serious error, indicating that the program itself may be unable to continue running.

    :param
    name: logger name - it will be the aplication name
    type:<string>
    log_file: log filename - path to log file name
    type:<string>
    level: level could be INFO, DEBUG etc....
            check documentation. IF model is INFO it will not log debug messages
    type:<string
    return:
    logger:when we need to log to file we will use this object.
    type:<class 'logging.Logger'>
    EXAMPLE usage : logger.debug("message)
                or
                logger.info("MESSAGE)
                or
                logger.error("MESSAGE)
                or
                logger.warning("MESSAGE)
    """
    # Bytes to Megabytes converter(FOR REFERENCING):
    #   bytes:50000000 == 50 MB(in decimal)
    #   bytes:50000000 == 47.6837158203125 MB (in binary)
    #   20000000 Bytes = 20 MB (in decimal)
    #   20000000 Bytes = 19.073486328125 MB (in binary)
    # DEFINE DEFAULT VALUES FOR LOG, IN CASE THEY DON'T EXIST IN config.py
    if max_size is None:
        max_size = 20000000
    if number_of_backup_files_to_store is None:
        number_of_backup_files_to_store = 10

    # ?????
    if level is None:
        level = logging.INFO

    # CHECK IF DIRECTORY EXISTS (WE WANTO TO STORE LOG FILES HERE)
    if path.exists("LOGS") is False:
        print("Make directory: LOGS")
        mkdir("LOGS")

    # OLD CONFIGURATION
    # relative_log_path_name = "LOGS" + "/" + log_file_name

    # CHECK Logging documentation for details
    # OLD FORMAT OUTPUT FOR LOGGING - LESS VERBOSE
    # formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    ##logger = logging.getLogger(name)
    ##formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    ##logger.name = name
    ##logger.setLevel(level)
    # add a rotating handler
    ##handler = RotatingFileHandler(filename=log_file_name,
    #                              mode="a",
    #                              maxBytes=max_size,
    #                              backupCount=number_of_backup_files_to_store)
    ##handler.setFormatter(formatter)
    ##logger.addHandler(handler)

    #####
    logger = logging.getLogger(name=name)
    logger.setLevel(level=level)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(filename=log_file_name)
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger


# THIS IS NOT IN USE - WE CAN DELETE THIS- just a test . we have a function with this name in file: "manage_logs"
def check_if_is_json():
    print("OUTPUT - Starting function check_if_is_json")
    # CHECK IF CONTENT IS 'application/json' - (for cases that clients try to send us xml ou html or javascript or ...)
    if request.headers['Content-Type'] != 'application/json':
        raise DataError("Please , send us Json data.")

    # LOAD JSON DATA FROM CLIENT
    try:
        data = request.json
    # Catch exceptions - Client doesn't send us json data or json dictionary is not well formatted"
    # For specific dictionary keys and values present in the data dictionary  we will check them later
        return data
    except Exception as error:
        raise DataError("Please , send us Json data.")
