#from the_app import app
from json import dumps, dump
from flask import request, jsonify, request, Blueprint, current_app, make_response
from datetime import datetime
from the_app.request_data import get_http_request_info, request_data, InvalidUsage
from the_app.manage_logs import NetworkAutomateLogs
from the_app.connect import ConnectToDevice
from flask import current_app

# HOW TO USE THIS
from werkzeug.exceptions import HTTPException, InternalServerError

"""
This file contains the Views/routes
Existing Views:
    /
    /index
    /add_list_of_commands
    /add_command_raw
    /add_command_raw_not_privileged
    /save_running_configurations
    /configure_multiple_devices
"""

# TODO: WE have to DECIDE IF WE WANT TO LOG ALL print(messages) in "debug" or "info" mode
#  - In view add_raw_command, the logger were used in 'info' mode. In other Views We did not setup the logger.
#  (write to log)
#  rationale:
#  1. We will use LOGS/NetworkAutomateJsonlog.log to reveal just the operation status.
#        - if a response to a request on webservice was on status: Failure or Success
#  2. The file LOGS/NetworkAutomate.log will have just th info and warnings.
#  3. on INFO mode only ...
#     The file LOGS/debug_NetworkAutomate.log will have all the operations being done on requests when
#         FLASK_ENV=development

# TODO: WE NEED TO LEARN:
#    - HOW USE SETUP TOOLS
#    - USE THE FLASK APPLICATION FACTORY PATTERN ....                       DONE  OK!
#    - Deploy on Gunicorn. Source: https://gunicorn.org/                    DONE OK!  --> done in Centos7 Server
#    - WEB proxy nginx.                                                     DONE OK!  --> done in Centos7 Server
#    - Deploy APP on DOCKER.
#    - Do more unittesting.


# CREATE A BLUEPRINT
api = Blueprint("api", __name__)


# register the in the blueprint
@api.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


# https://flask.palletsprojects.com/en/1.1.x/errorhandling/
# It is possible to register error handlers for very generic base classes such as HTTPException or even Exception.
# However, be aware that these will catch more than you might expect.
# An error handler for HTTPException might be useful for turning the default HTML errors pages into JSON, for example.

# HOW TO MAKE THIS GLOBAL
# SINCE THIS A HTTP ERROR FOR OUR FLASK APP we will register the errors in the __init__ file and not in the blueprint
#@api.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    error_dict ={"code": e.code,
                 "name": e.name,
                 "description": e.description,

    }
    response.content_type = "application/json"

    # CREATE ERROR OBJECT for logging in the: >>> .json file and .log file
    client_info = get_http_request_info(request)
    start_time = end_time = datetime.now()
    logger_obj = NetworkAutomateLogs(start_time=start_time, end_time=end_time, elapsed_time=0, client_info=client_info,
                                     logger_engine=current_app.logger,
                                     user_data_for_logging=None)
    logger_obj.http_errors_met(error_dict)
    # CREATE A JSON LOG
    logger_obj.create_json_log()
    return response


#@api.errorhandler(Exception)
def internal_server_error(error):


    """Return JSON instead of HTML for Internal Server Errors."""

    if isinstance(error, HTTPException):
        client_info = get_http_request_info(request)

        current_app.logger.error(client_info)
        # start with the correct headers and status code from the error
        response = error.get_response()
        # replace the body with JSON
        response.data = dumps({
            "code": error.code,  #
            "name": error.name,
            "description": error.description,
        })
        error_dict = {"code": error.code,
                      "name": error.name,
                      "description": error.description,

                      }
        response.content_type = "application/json"

        # CREATE ERROR OBJECT for logging in the: >>> .json file and .log file
        client_info = get_http_request_info(request)
        start_time = end_time = datetime.now()
        logger_obj = NetworkAutomateLogs(start_time=start_time, end_time=end_time, elapsed_time=0, client_info=client_info,
                                         logger_engine = current_app.logger,
                                         user_data_for_logging=None)
        logger_obj.http_errors_met(error_dict)
        # CREATE A JSON LOG
        logger_obj.create_json_log()
        return response

    # NOT AN HTTP ERROR.  HERE WE WILL CAUGHT 501 internal server errors
    print(dir(error))
    print(type(error))
    print(error)

    client_info = get_http_request_info(request)

    current_app.logger.error(client_info)

    error_dict = {"code": 500,
                  "name": "INTERNAL SERVER ERROR",
                  "description": str(error),

                 }
    response_to_client_dict = {"code": 500,
                               "name": "INTERNAL SERVER ERROR",
                               "description": "Sorry, We can't continue. Try again later or contact System Admin.",
                               }

    response = {'NETWORK_AUTOMATE_RESPONSE': response_to_client_dict}
    #response_to_client = {"NETWORK_AUTOMATE_RESPONSE": error_dict}
    # CREATE ERROR OBJECT for logging in the: >>> .json file and .log file
    client_info = get_http_request_info(request)
    start_time = end_time = datetime.now()
    logger_obj = NetworkAutomateLogs(start_time=start_time, end_time=end_time, elapsed_time=0, client_info=client_info,
                                     logger_engine=current_app.logger,
                                     user_data_for_logging=None)
    logger_obj.http_errors_met(error_dict)
    # CREATE A JSON LOG
    logger_obj.create_json_log()
    return response_to_client_dict, 500



# DEACTIVATE THIS ROUTES ON PRODUCTION
@api.route('/')
def index():
    """
    # just a testing VIEW
    :return:
    """
    data = {"app_name": "NETWORKAUTOMATE",
            "status": "Development",
            "author":'Nuno Moura',
            "email": "nm.10000.testes@gmail.com",
            "coordination": ["Alexandre Santos", "Pedro Vapi"],
            "copyright": None
            }
    return dumps(data, indent=4)


@api.route("/add_command_raw", methods=["POST"])
def controller_add_raw_commands():
    """
    This view allows a client to send a raw command to a cisco device in PRIVILEGED  mode
    :return: <dict> result of the operation. check documentation for details
    """
    print("OUTPUT - Entering function: controller_add_raw_commands")
    current_app.logger.info("OUTPUT - Entering function: controller_add_raw_commands")
    # START COUNTING TIME FOR LOGGING PURPOSES
    start_time = datetime.now()

    # GETTING CLIENT INFO, FOR LOGGING
    client_info = get_http_request_info(request)

    # OUTPUT MESSAGES IN DEBUG MODE- ( WE CAN CREATE A DEBUG MODE FOR LOGGING )
    message = "OUTPUT - WEBSERVICE URI: \t'{}'".format(client_info["REQUEST_URI"])
    current_app.logger.debug(message)
    message = ("OUTPUT - REQUEST_INFORMATION " + str(client_info))
    current_app.logger.debug(message)
    current_app.logger.debug("OUTPUT - Let´s request data from client - CHECK IF DATA IS VALID")
    data = request_data(client_info)

    # CHECK request_data output for detail--> we will try to find here: ERROR 1, 2, 3
    current_app.logger.debug("OUTPUT - data: {} ".format(data))
    if isinstance(data[0], dict):
        if data[0]["STATUS"] == "Failure":
            current_app.logger.debug("OUTPUT - WE HAVE FOUND AN ERROR......")
            end_time = datetime.now()
            total_time = end_time - start_time
            if data[0]["ERROR"] == "1":
                current_app.logger.debug("OUTPUT - ERROR 1. LETS RAISE INVALID_USAGE function amd inform client ")
                current_app.logger.debug("OUTPUT - data: {}".format(data))
                # CREATE ERROR OBJECT
                logger_obj = NetworkAutomateLogs(start_time, end_time, total_time, client_info,  current_app.logger,
                                                 user_data_for_logging= None)
                # CALL METHOD FOR ERROR 1 ( CHECK ERROR-CATALOG.txt for details )
                logger_obj.error_1_json_data(data[0])
                # CREATE A JSON LOG
                logger_obj.create_json_log()
                raise InvalidUsage("Bad request!", status_code=400, payload=logger_obj.error_dict)
            if data[0]["ERROR"] == "2":
                current_app.logger.debug("OUTPUT - ERROR 2. LETS RAISE INVALID_USAGE function amd inform client ")
                current_app.logger.debug("OUTPUT - data: {}".format(data))
                # CREATE ERROR OBJECT
                logger_obj = NetworkAutomateLogs(start_time, end_time, total_time, client_info,  current_app.logger,
                                                 user_data_for_logging=data[1])
                # CALL METHOD FOR ERROR 2 ( CHECK ERROR-CATALOG.txt for details
                logger_obj.error_2_fundamental_data_required(data[0])
                # CREATE A JSON LOG
                logger_obj.create_json_log()
                raise InvalidUsage("Bad request!", status_code=400, payload=logger_obj.error_dict)
            if data[0]["ERROR"] == "3":
                current_app.logger.debug("OUTPUT - ERROR 3. LETS RAISE INVALID_USAGE function amd inform client ")
                current_app.logger.debug("OUTPUT - data: {}".format(data))
                # CREATE ERROR OBJECT
                #EXAMPLE HOW DATA SHOULD BE :OUTPUT - \
                # data ({'STATUS': 'Failure', 'ERROR': '3', 'TYPE': 'WEBSERVICE DATA FAILURE', 'MESSAGE':
                # 'Please, send an ip key in your dictionary'}, {'ips': '192.168.7.1'}) ------   -------    is a tuple
                logger_obj = NetworkAutomateLogs(start_time, end_time, total_time, client_info,  current_app.logger,
                                                 user_data_for_logging=data[1])
                # CALL METHOD FOR ERROR 3 ( CHECK ERROR-CATALOG.txt for details
                logger_obj.error_webservice_data_failure(data[0])
                # CREATE A JSON LOG
                logger_obj.create_json_log()
                raise InvalidUsage("Bad request!", status_code=400, payload=logger_obj.error_dict)

    # SINCE ERROR 1, 2 and 3 were not found it means data is OK!
    line = "=" * 79
    current_app.logger.debug(line)
    current_app.logger.debug("OUTPUT - data is OK! ")
    current_app.logger.debug("OUTPUT - data[0]: {}".format(data[0]))
    current_app.logger.debug("OUTPUT - data[1]: {}".format(data[1]))
    current_app.logger.debug(line)

    # CHECK IF IS PORT
    # MAKE A COPY OF CLIENT DATA for logging purposes
    user_data_for_logging = dict((k, v) for k, v in data[2].items())
    current_app.logger.debug("OUTPUT - user_data_for_logging: {}".format(user_data_for_logging))

    # LETS REMOVE THE KEYS, VLAN_ID AND VLAN_NAME AND STORE THEIR VALUES ON NEW VARIABLES. Construct a dictionary with
    # vlan_id an vlan_name send later. there are a case where client doesn 't send to US vlan_name and we
    # have to process theses kind of behavior
    command_to_send = data[1].pop("command_to_send")
    current_app.logger.debug("OUTPUT - command_list_to_send: {}".format(command_to_send))

    # CHECK IF CLIENT WANTS A SPECIFIC PORT FOR CONNECTION to device. SET TO NONE if not
    if isinstance(data[1], dict):
        if 'port' in data[1].keys():
            port = data[1].pop("port")
        else:
            port = None

    if data[0]["CONNECTIONS"] == "both":
        current_app.logger.debug("OUTPUT - CLIENT WANT US TO PERFORM A TRY, ON BOTH CONNECTIONS: TELNET AND SSH")
        #  -------  first try a telnet connection ---------------
        current_app.logger.debug("OUTPUT - first try a telnet connection")
        connection = ConnectToDevice(data[1], connection_type="TELNET", port=port)

        current_app.logger.debug("OUTPUT - LETS START CONFIGURING")
        # LETS START CONFIGURING
        result = connection.configure_add_raw_commands(command_to_send=command_to_send)
        current_app.logger.debug("OUTPUT - result of telnet connection: {}".format(result))
        current_app.logger.debug("OUTPUT - type(result): {}".format(type(result)))
        current_app.logger.debug("OUTPUT - result is a list with one dictionary unstructured data")

        result_telnet = result
        end_time = datetime.now()
        total_time = end_time - start_time
        # - ------- At these point we should check if telnet was successful ---------------------
        if isinstance(result_telnet, dict):
            if result_telnet["STATUS"] == "Failure":
                del connection
                current_app.logger.debug("OUTPUT - Perform a ssh connection because telnet failed ")
                # -- ------ Perform a ssh connection because telnet failed ----------

                connection_new = ConnectToDevice(data[1], connection_type="SSH", port=port)
                # LETS START CONFIGURING
                result = connection_new .configure_add_raw_commands(command_to_send=command_to_send)
                result_ssh = result
                current_app.logger.debug("OUTPUT - result of ssh connection: {} ".format(result))
                current_app.logger.debug("OUTPUT - type(result): ".format(type(result)))
                current_app.logger.debug("OUTPUT - result is a list with one dictionary unstructured data")

                if isinstance(result, dict):
                    # ---- Check if ssh connection was successful. if not, inform client of both fails and log
                    if result["STATUS"] == "Failure":
                        # Expecting here to appear error 4 -------- HANDLE ERROR
                        # first handle error 4
                        if result["ERROR"] == "4":
                            # CREATE ERROR OBJECT
                            logger_obj = NetworkAutomateLogs(start_time, end_time, total_time, client_info,
                                                             current_app.logger,
                                                             user_data_for_logging=user_data_for_logging)
                            # CALL METHOD FOR BOTH CONNECTION ERROR
                            logger_obj.error_both_connection_fails("Failed connection to device", result_ssh, result_telnet)
                            # CREATE A JSON LOG
                            logger_obj.create_json_log()
                            current_app.logger.debug("OUTPUT - result: {}".format(result))
                            raise InvalidUsage("Bad request!", status_code=513, payload=logger_obj.error_dict)
                        # Error 8 FOR NOW THESE ERROR DOESN`T  EXIST YET - LATER WE MAY NEED IT
                        # if result["ERROR"] == "8":
                        # CREATE ERROR OBJECT
                        #    logger_obj = NetworkAutomateLogs(start_time, end_time, total_time, client_info, logger_engine,
                        #                                     user_data_for_logging=user_data_for_logging)
                        # CALL METHOD FOR ERROR
                        #    logger_obj.error_operation_error(result)
                        # CREATE A JSON LOG
                        #    logger_obj.create_json_log()
                        #    raise InvalidUsage("Bad request!", status_code=513, payload=logger_obj.error_dict)

        #  -----  ----- connection to device Successful.   ------ Build log and return info to client ----
        # Connection to device:Successful. OPERATION SUCCESSFUL  ------ Build log and return interface config to client ----
        # --------- CREATE success LOG -------
        logger_obj = NetworkAutomateLogs(start_time, end_time, total_time, client_info,  current_app.logger,
                                         user_data_for_logging=user_data_for_logging)
        success_dict = {"STATUS": "Success",
                        "MESSAGE": "Check results. Whenever possible, we will try to output Structured and Unstructured "
                                   "data "
                                   "captured from de Network Device CLI. We have to be careful on what commands we are "
                                   "trying to send, because we are not in privileged mode, and sometimes we are not "
                                   "authorized to run them on the device and the output will be something like: e.g.( "
                                   " ^\n% Invalid input detected at '^' marker.\n )",
                        "STRUCTURED_RESULT": result[0],
                        "UNSTRUCTURED_RESULT": result[1]
                        }

        current_app.logger.debug("OUTPUT - returning...  RESPONSE TO CLIENT")
        final_dict = {"NETWORK AUTOMATE RESPONSE": success_dict}
        # CALL METHOD FOR success messages
        logger_obj.sucess_add_raw_commands(success_dict)
        # CREATE A JSON LOG
        logger_obj.create_json_log()

        # GIVE RESPONSE TO VIEW, for client
        return final_dict

    # What differ a ssh or telnet connection is only the device driver used by netmiko, so the first thing we should do,
    # is to know which connection the client want us to perform.
    #  ------   we will pass these choice to the class "ConnectToDevice". it will handle the choice for us
    current_app.logger.debug("OUTPUT - CLIENT WANT US TO PERFOR A SPECIFIC CONNECTION- it will be telnet or ssh")

    if data[0]["CONNECTIONS"] == "telnet":
        current_app.logger.debug("OUTPUT - force telnet")
        connection = ConnectToDevice(data=data[1], connection_type="TELNET", port=port)
    if data[0]["CONNECTIONS"] == "ssh":
        current_app.logger.debug("OUTPUT - force ssh")
        connection = ConnectToDevice(data=data[1], connection_type="SSH", port=port)

    # LETS START CONFIGURING
    current_app.logger.debug("OUTPUT - Starting to configure")
    result = connection.configure_add_raw_commands(command_to_send=command_to_send)
    # "OUTPUT - result[0] is a list with one dictionary with structured data and a dictionary with unstructured data")
    current_app.logger.debug("OUTPUT - configure_add_raw_commands ended ....")
    current_app.logger.debug(line)
    current_app.logger.debug("OUTPUT - result: {}".format(result))
    current_app.logger.debug("OUTPUT - type(result): {} ".format(type(result)))
    # TIME FOR LOGGING PURPOSES
    end_time = datetime.now()
    total_time = end_time - start_time


    # ---- At these point, if the connection object return an error ( like connection error or other ) we should
    # report these and inform client
    if isinstance(result, dict):
        if result["STATUS"] == "Failure":
            # if status is failure , we are EXPECTING HERE ERROR 4
            # first Error 4
            current_app.logger.debug("OUTPUT - FOUND A ERROR --> result: {}".format(result))

            if result["ERROR"] == "4":
                # CREATE ERROR OBJECT
                logger_obj = NetworkAutomateLogs(start_time, end_time, total_time, client_info,  current_app.logger,
                                                 user_data_for_logging=user_data_for_logging)
                # CALL METHOD FOR ERROR
                logger_obj. error_netmiko(result)
                # CREATE A JSON LOG
                logger_obj.create_json_log()
                raise InvalidUsage("Bad request!", status_code=512, payload=logger_obj.error_dict)

    # Connection to device:Successful. OPERATION SUCCESSFUL  ------ Build log and return interface config to client ----
    # --------- CREATE success LOG -------
    logger_obj = NetworkAutomateLogs(start_time, end_time, total_time, client_info,  current_app.logger,
                                     user_data_for_logging=user_data_for_logging)

    success_dict = {"STATUS": "Success",
                    "MESSAGE": "Check results. Whenever possible, we will try to output Structured and Unstructured data"
                               " captured from de Network Device CLI. We have to be careful on what commands we are "
                               "trying to send, because we are not in privileged mode, and sometimes we are not "
                               "authorized to run them on the device and the output will be something like: e.g.( "
                               " ^\n% Invalid input detected at '^' marker.\n )",
                    "STRUCTURED_RESULT": result[0],
                    "UNSTRUCTURED_RESULT": result[1]
                    }
    current_app.logger.debug("OUTPUT - operation successful - returning data to client")
    final_dict = {"NETWORK AUTOMATE RESPONSE": success_dict}
    # CALL METHOD FOR success messages
    logger_obj.sucess_add_raw_commands(success_dict)
    # CREATE A JSON LOG
    logger_obj.create_json_log()

    # GIVE RESPONSE to client
    return final_dict


@api.route("/add_list_of_commands", methods=["POST"])
def controller_add_list_off_commands_to_device():
    """
    Allows a client to send list of commands to cisco network device.
    :return: <dictionary> result of the operation . Check documentation for more details
    """
    # TODO: convert print screens to app.logger.debug("message")

    print("OUTPUT - Entering function: controller_add_list_off_commands_to_device")
    # START COUNTING TIME FOR LOGGING PURPOSES
    start_time = datetime.now()

    # GETTING CLIENT INFO, FOR LOGGING
    client_info = get_http_request_info(request)

    # OUTPUT MESSAGES IN DEBUG MODE- ( WE CAN CREATE A DEBUG MODE FOR LOGGING )
    message = "OUTPUT - WEBSERVICE URI: \t'{}'".format(client_info["REQUEST_URI"])
    print(message)
    message = ("OUTPUT - REQUEST_INFORMATION " + str(client_info))
    # ----- --- Below line is just to remember us that we could create a debug mode log with messages like these one.
    # logger_engine.debug(message)
    print("OUTPUT - starting time: {}".format(start_time))
    print(message)

    print("OUTPUT - Let´s request data from client - CHECK IF DATA IS VALID")
    data = request_data(client_info)
    print("OUTPUT - data: ", data)
    if isinstance(data[0], dict):
        if data[0]["STATUS"] == "Failure":
            print("OUTPUT - WE HAVE FOUND AN ERROR......")
            end_time = datetime.now()
            total_time = end_time - start_time
            if data[0]["ERROR"] == "1":
                print("OUTPUT - ERROR 1. LETS RAISE INVALID_USAGE function amd inform client ")
                print("OUTPUT - data", data)
                # CREATE ERROR OBJECT
                logger_obj = NetworkAutomateLogs(start_time, end_time, total_time, client_info,  current_app.logger,
                                                 user_data_for_logging= None)
                # CALL METHOD FOR ERROR 1 ( CHECK ERROR-CATALOG.txt for details )
                logger_obj.error_1_json_data(data[0])
                # CREATE A JSON LOG
                logger_obj.create_json_log()
                raise InvalidUsage("Bad request!", status_code=400, payload=logger_obj.error_dict)
            if data[0]["ERROR"] == "2":
                print("OUTPUT - ERROR 2. LETS RAISE INVALID_USAGE function amd inform client ")
                print("OUTPUT - data", data)
                # CREATE ERROR OBJECT
                logger_obj = NetworkAutomateLogs(start_time, end_time, total_time, client_info,  current_app.logger,
                                                 user_data_for_logging=data[1])
                # CALL METHOD FOR ERROR 2 ( CHECK ERROR-CATALOG.txt for details
                logger_obj.error_2_fundamental_data_required(data[0])
                # CREATE A JSON LOG
                logger_obj.create_json_log()
                raise InvalidUsage("Bad request!", status_code=400, payload=logger_obj.error_dict)
            if data[0]["ERROR"] == "3":
                print("OUTPUT - ERROR 3. LETS RAISE INVALID_USAGE function amd inform client ")
                print("OUTPUT - data", data)
                # CREATE ERROR OBJECT
                #EXAMPLE HOW DATA SHOULD BE :OUTPUT - \
                # data ({'STATUS': 'Failure', 'ERROR': '3', 'TYPE': 'WEBSERVICE DATA FAILURE', 'MESSAGE':
                # 'Please, send an ip key in your dictionary'}, {'ips': '192.168.7.1'}) ------   -------    is a tuple
                logger_obj = NetworkAutomateLogs(start_time, end_time, total_time, client_info,  current_app.logger,
                                                 user_data_for_logging=data[1])
                # CALL METHOD FOR ERROR 3 ( CHECK ERROR-CATALOG.txt for details
                logger_obj.error_webservice_data_failure(data[0])
                # CREATE A JSON LOG
                logger_obj.create_json_log()
                raise InvalidUsage("Bad request!", status_code=400, payload=logger_obj.error_dict)

    print("=" * 79)
    print("OUTPUT - data is OK! ")
    print("OUTPUT - data[0]", data[0])  # OUTPUT - data[0]: {'STATUS': 'Success', 'CONNECTIONS': 'both'}
    print("OUTPUT - data[1]", data[1])  # OUTPUT - data[1]: {'ip': '192.168.2.245'}
    print("=" * 79)
    # CHECK IF IS PORT
    # MAKE A COPY OF CLIENT DATA for logging purposes
    user_data_for_logging = dict((k, v) for k, v in data[2].items())
    print("OUTPUT - user_data_for_logging:", user_data_for_logging)

    # LETS REMOVE THE KEYS, VLAN_ID AND VLAN_NAME AND STORE THEIR VALUES ON NEW VARIABLES. Construct a dictionary with
    # vlan_id an vlan_name send later. there are a case where client doesn 't send to US vlan_name and we
    # have to process theses kind of behavior
    command_list_to_send = data[1].pop("commands_list")
    print("OUTPUT - command_list_to_send: {}".format(command_list_to_send))

    # CHECK IF CLIENT WANTS A SPECIFIC PORT FOR CONNECTION to device. SET TO NONE if not
    if isinstance(data[1], dict):
        if 'port' in data[1].keys():
            port = data[1].pop("port")
        else:
            port = None

    if data[0]["CONNECTIONS"] == "both":
        #  -------  first try a telnet connection ---------------
        connection = ConnectToDevice(data[1], connection_type="TELNET", port=port)
        # LETS START CONFIGURING
        result = connection.configure_add_commands_list(commands_list=command_list_to_send)

        # result = connection.get_show_run()
        print("OUTPUT - result of telnet connection: ", result)
        print("OUTPUT - type(result): ", type(result))
        print("OUTPUT - result is a list with one dictionary unstructured data")
        result_telnet = result
        end_time = datetime.now()
        total_time = end_time - start_time
        # - ------- At these point we should check if telnet was successful ---------------------
        if isinstance(result_telnet, dict):
            if result_telnet["STATUS"] == "Failure":
                del connection
                # -- ------ Perform a ssh connection because telnet failed ----------

                connection = ConnectToDevice(data[1], connection_type="SSH", port=port)
                # LETS START CONFIGURING
                result = connection.configure_add_commands_list(commands_list=command_list_to_send)

                print("OUTPUT - result of ssh connection: ", result)
                print("OUTPUT - type(result): ", type(result))
                print("OUTPUT - result is a list with one dictionary unstructured data")
                result_ssh = result

                if isinstance(result, dict):
                    # ---- Check if ssh connection was successful. if not, inform client of both fails and log
                    if result["STATUS"] == "Failure":
                        # Expecting here to appear error 4 -------- HANDLE ERROR
                        # first handle error 4
                        if result["ERROR"] == "4":
                            # CREATE ERROR OBJECT
                            logger_obj = NetworkAutomateLogs(start_time, end_time, total_time, client_info,
                                                             current_app.logger,
                                                             user_data_for_logging=user_data_for_logging)
                            # CALL METHOD FOR BOTH CONNECTION ERROR
                            logger_obj.error_both_connection_fails("Failed connection to device", result_ssh, result_telnet)
                            # CREATE A JSON LOG
                            logger_obj.create_json_log()
                            print("OUTPUT - result: {}".format(result))
                            raise InvalidUsage("Bad request!", status_code=513, payload=logger_obj.error_dict)
                        # Error 8 FOR NOW THESE ERROR DOESN EXIST YET - LATER WE MAY NEED IT
                        # if result["ERROR"] == "8":
                        # CREATE ERROR OBJECT
                        #    logger_obj = NetworkAutomateLogs(start_time, end_time, total_time, client_info, logger_engine,
                        #                                     user_data_for_logging=user_data_for_logging)
                        # CALL METHOD FOR ERROR
                        #    logger_obj.error_operation_error(result)
                        # CREATE A JSON LOG
                        #    logger_obj.create_json_log()
                        #    raise InvalidUsage("Bad request!", status_code=513, payload=logger_obj.error_dict)

        #  -----  ----- connection to device Successful.   ------ Build log and return info to client ----
        # Connection to device:Successful. OPERATION SUCCESSFUL  ------ Build log and return interface config to client ----
        # --------- CREATE success LOG -------
        logger_obj = NetworkAutomateLogs(start_time, end_time, total_time, client_info,  current_app.logger,
                                         user_data_for_logging=user_data_for_logging)

        success_dict = {"STATUS": "Success",
                        "MESSAGE": "We sent commands to device .Check network device cli to confirm. Since there "
                                   "a multiple commands and multiple outputs its difficult to search for a pattern "
                                   "error. Check network device cli to confirm that the commands did not result in "
                                   "errors. ",
                        "RESULT_OUTPUT_CLI": result
                        }

        final_dict = {"NETWORK AUTOMATE RESPONSE": success_dict}
        # CALL METHOD FOR success messages
        logger_obj.sucess_add_raw_commands(success_dict)
        # CREATE A JSON LOG
        logger_obj.create_json_log()

        # GIVE RESPONSE TO VIEW, for client
        return final_dict

    # What differ a ssh or telnet connection is only the device driver used by netmiko, so the first thing we should do,
    # is to know which connection the client want us to perform.
    #  ------   we will pass these choice to the class "ConnectToDevice". ---------------
    if data[0]["CONNECTIONS"] == "telnet":
        connection = ConnectToDevice(data=data[1], connection_type="TELNET", port=port)
    if data[0]["CONNECTIONS"] == "ssh":
        connection = ConnectToDevice(data=data[1], connection_type="SSH", port=port)

    # LETS START CONFIGURING
    result = connection.configure_add_commands_list(commands_list=command_list_to_send)
    print("OUTPUT - configure_add_raw_commands ended ....")
    print("="*79)
    print("OUTPUT - result: ", result)
    print("OUTPUT - type(result): ", type(result))
    # "OUTPUT - result[0] is a list with one dictionary with structured data and a dictionary with unstructured data")

    # TIME FOR LOGGING PURPOSES
    end_time = datetime.now()
    total_time = end_time - start_time


    # ---- At these point, if the connection object return an error ( like connection error or other ) we should
    # report these and inform client
    if isinstance(result, dict):
        if result["STATUS"] == "Failure":
            # if status is failure , we are EXPECTING HERE ERROR 4, 3 or 6
            # first Error 4
            if result["ERROR"] == "4":
                # CREATE ERROR OBJECT
                logger_obj = NetworkAutomateLogs(start_time, end_time, total_time, client_info,  current_app.logger,
                                                 user_data_for_logging=user_data_for_logging)
                # CALL METHOD FOR ERROR
                logger_obj. error_netmiko(result)
                # CREATE A JSON LOG
                logger_obj.create_json_log()
                raise InvalidUsage("Bad request!", status_code=512, payload=logger_obj.error_dict)
            # Error 8 FOR NOW THESE ERROR DOESN EXIST YET - LATER WE MAY NEED IT
            #if result["ERROR"] == "8":
                # CREATE ERROR OBJECT
            #    logger_obj = NetworkAutomateLogs(start_time, end_time, total_time, client_info, logger_engine,
            #                                     user_data_for_logging=user_data_for_logging)
                # CALL METHOD FOR ERROR
            #    logger_obj.error_operation_error(result)
                # CREATE A JSON LOG
            #    logger_obj.create_json_log()
            #    raise InvalidUsage("Bad request!", status_code=513, payload=logger_obj.error_dict)


    # Connection to device:Successful. OPERATION SUCCESSFUL  ------ Build log and return interface config to client ----
    # --------- CREATE success LOG -------
    logger_obj = NetworkAutomateLogs(start_time, end_time, total_time, client_info,  current_app.logger,
                                     user_data_for_logging=user_data_for_logging)

    success_dict = {"STATUS": "Success",
                    "MESSAGE": "Check network device cli output to confirm.",
                    "RESULT_OUTPUT_CLI": result
                    }

    final_dict = {"NETWORK AUTOMATE RESPONSE": success_dict}
    # CALL METHOD FOR success messages
    logger_obj.sucess_add_raw_commands(success_dict)
    # CREATE A JSON LOG
    logger_obj.create_json_log()

    # GIVE RESPONSE TO VIEW, for client
    return final_dict


@api.route('/save_running_configurations', methods=["POST"])
def save_run_conf():
    """
    This view allows a client to save the running configurations to strartup configgurations on a cisco netwrkdevice
    :return: <dictionary> result of the operation. Check documentation for more details.
    """
    # TODO: convert print screens to app.logger.debug("message")
    print("OUTPUT - Entering function: SaveRunning_config")
    # START COUNTING TIME FOR LOGGING PURPOSES
    start_time = datetime.now()

    # GETTING CLIENT INFO, FOR LOGGING
    client_info = get_http_request_info(request)

    # OUTPUT MESSAGES IN DEBUG MODE- ( WE CAN CREATE A DEBUG MODE FOR LOGGING )
    message = "OUTPUT - WEBSERVICE URI: \t'{}'".format(client_info["REQUEST_URI"])
    print(message)
    message = ("OUTPUT - REQUEST_INFORMATION " + str(client_info))
    # ----- --- Below line is just to remember us that we could create a debug mode log with messages like these one.
    # logger_engine.debug(message)
    print("OUTPUT - starting time: {}".format(start_time))
    print(message)

    print("OUTPUT - Let´s request data from client - CHECK IF DATA IS VALID")
    data = request_data(client_info)
    print("OUTPUT - data: ", data)
    if isinstance(data[0], dict):
        if data[0]["STATUS"] == "Failure":
            print("OUTPUT - WE HAVE FOUND AN ERROR......")
            end_time = datetime.now()
            total_time = end_time - start_time
            if data[0]["ERROR"] == "1":
                print("OUTPUT - ERROR 1. LETS RAISE INVALID_USAGE function amd inform client ")
                print("OUTPUT - data", data)
                # CREATE ERROR OBJECT
                logger_obj = NetworkAutomateLogs(start_time, end_time, total_time, client_info, current_app.logger,
                                                 user_data_for_logging=None)
                # CALL METHOD FOR ERROR 1 ( CHECK ERROR-CATALOG.txt for details )
                logger_obj.error_1_json_data(data[0])
                # CREATE A JSON LOG
                logger_obj.create_json_log()
                raise InvalidUsage("Bad request!", status_code=400, payload=logger_obj.error_dict)
            if data[0]["ERROR"] == "2":
                print("OUTPUT - ERROR 2. LETS RAISE INVALID_USAGE function amd inform client ")
                print("OUTPUT - data", data)
                # CREATE ERROR OBJECT
                logger_obj = NetworkAutomateLogs(start_time, end_time, total_time, client_info, current_app.logger,
                                                 user_data_for_logging=data[1])
                # CALL METHOD FOR ERROR 2 ( CHECK ERROR-CATALOG.txt for details
                logger_obj.error_2_fundamental_data_required(data[0])
                # CREATE A JSON LOG
                logger_obj.create_json_log()
                raise InvalidUsage("Bad request!", status_code=400, payload=logger_obj.error_dict)
            if data[0]["ERROR"] == "3":
                print("OUTPUT - ERROR 3. LETS RAISE INVALID_USAGE function amd inform client ")
                print("OUTPUT - data", data)
                # CREATE ERROR OBJECT
                # EXAMPLE HOW DATA SHOULD BE :OUTPUT - \
                # data ({'STATUS': 'Failure', 'ERROR': '3', 'TYPE': 'WEBSERVICE DATA FAILURE', 'MESSAGE':
                # 'Please, send an ip key in your dictionary'}, {'ips': '192.168.7.1'}) ------   -------    is a tuple
                logger_obj = NetworkAutomateLogs(start_time, end_time, total_time, client_info, current_app.logger,
                                                 user_data_for_logging=data[1])
                # CALL METHOD FOR ERROR 3 ( CHECK ERROR-CATALOG.txt for details
                logger_obj.error_webservice_data_failure(data[0])
                # CREATE A JSON LOG
                logger_obj.create_json_log()
                raise InvalidUsage("Bad request!", status_code=400, payload=logger_obj.error_dict)

    print("=" * 79)
    print("OUTPUT - data is OK! ")
    print("OUTPUT - data[0]", data[0])  # OUTPUT - data[0]: {'STATUS': 'Success', 'CONNECTIONS': 'both'}
    print("OUTPUT - data[1]", data[1])  # OUTPUT - data[1]: {'ip': '192.168.2.245'}
    print("=" * 79)
    # CHECK IF IS PORT
    # MAKE A COPY OF CLIENT DATA for logging purposes
    user_data_for_logging = dict((k, v) for k, v in data[2].items())
    print("OUTPUT - user_data_for_logging:", user_data_for_logging)

    # LETS REMOVE THE KEYS, VLAN_ID AND VLAN_NAME AND STORE THEIR VALUES ON NEW VARIABLES. Construct a dictionary with
    # vlan_id an vlan_name send later. there are a case where client doesn 't send to US vlan_name and we
    # have to process theses kind of behavior
    #command_list_to_send = data[1].pop("commands_list")
    #print("OUTPUT - command_list_to_send: {}".format(command_list_to_send))

    # CHECK IF CLIENT WANTS A SPECIFIC PORT FOR CONNECTION to device. SET TO NONE if not
    if isinstance(data[1], dict):
        if 'port' in data[1].keys():
            port = data[1].pop("port")
        else:
            port = None

    if data[0]["CONNECTIONS"] == "both":
        #  -------  first try a telnet connection ---------------
        connection = ConnectToDevice(data[1], connection_type="TELNET", port=port)
        # LETS START CONFIGURING
        result = connection.save_running_config()

        # result = connection.get_show_run()
        print("OUTPUT - result of telnet connection: ", result)
        print("OUTPUT - type(result): ", type(result))
        print("OUTPUT - result is a list with one dictionary unstructured data")
        result_telnet = result
        end_time = datetime.now()
        total_time = end_time - start_time
        # - ------- At these point we should check if telnet was successful ---------------------
        if isinstance(result_telnet, dict):
            if result_telnet["STATUS"] == "Failure":
                del connection
                # -- ------ Perform a ssh connection because telnet failed ----------

                connection = ConnectToDevice(data[1], connection_type="SSH", port=port)
                # LETS START CONFIGURING
                result = connection.save_running_config()

                print("OUTPUT - result of ssh connection: ", result)
                print("OUTPUT - type(result): ", type(result))
                print("OUTPUT - result is a list with one dictionary unstructured data")
                result_ssh = result

                if isinstance(result, dict):
                    # ---- Check if ssh connection was successful. if not, inform client of both fails and log
                    if result["STATUS"] == "Failure":
                        # Expecting here to appear error 4 -------- HANDLE ERROR
                        # first handle error 4
                        if result["ERROR"] == "4":
                            # CREATE ERROR OBJECT
                            logger_obj = NetworkAutomateLogs(start_time, end_time, total_time, client_info,
                                                             current_app.logger,
                                                             user_data_for_logging=user_data_for_logging)
                            # CALL METHOD FOR BOTH CONNECTION ERROR
                            logger_obj.error_both_connection_fails("Failed connection to device", result_ssh,
                                                                   result_telnet)
                            # CREATE A JSON LOG
                            logger_obj.create_json_log()
                            print("OUTPUT - result: {}".format(result))
                            raise InvalidUsage("Bad request!", status_code=513, payload=logger_obj.error_dict)
                        # Error 8 FOR NOW THESE ERROR DOESN EXIST YET - LATER WE MAY NEED IT
                        # if result["ERROR"] == "8":
                        # CREATE ERROR OBJECT
                        #    logger_obj = NetworkAutomateLogs(start_time, end_time, total_time, client_info, logger_engine,
                        #                                     user_data_for_logging=user_data_for_logging)
                        # CALL METHOD FOR ERROR
                        #    logger_obj.error_operation_error(result)
                        # CREATE A JSON LOG
                        #    logger_obj.create_json_log()
                        #    raise InvalidUsage("Bad request!", status_code=513, payload=logger_obj.error_dict)

        #  -----  ----- connection to device Successful.   ------ Build log and return info to client ----
        # Connection to device:Successful. OPERATION SUCCESSFUL  ------ Build log and return interface config to client ----
        # --------- CREATE success LOG -------
        logger_obj = NetworkAutomateLogs(start_time, end_time, total_time, client_info, current_app.logger,
                                         user_data_for_logging=user_data_for_logging)

        success_dict = {"STATUS": "Success",
                        "MESSAGE": "Check network device cli output to confirm.",
                        "RESULT_OUTPUT_CLI": result
                        }

        final_dict = {"NETWORK AUTOMATE RESPONSE": success_dict}
        # CALL METHOD FOR success messages
        logger_obj.sucess_add_raw_commands(success_dict)
        # CREATE A JSON LOG
        logger_obj.create_json_log()

        # GIVE RESPONSE TO VIEW, for client
        return final_dict

    # What differ a ssh or telnet connection is only the device driver used by netmiko, so the first thing we should do,
    # is to know which connection the client want us to perform.
    #  ------   we will pass these choice to the class "ConnectToDevice". ---------------
    if data[0]["CONNECTIONS"] == "telnet":
        connection = ConnectToDevice(data=data[1], connection_type="TELNET", port=port)
    if data[0]["CONNECTIONS"] == "ssh":
        connection = ConnectToDevice(data=data[1], connection_type="SSH", port=port)

    # LETS send order to save running config to device
    result = connection.save_running_config()

    print("OUTPUT - configure_add_raw_commands ended ....")
    print("=" * 79)
    print("OUTPUT - result: ", result)
    print("OUTPUT - type(result): ", type(result))
    # "OUTPUT - result[0] is a list with one dictionary with structured data and a dictionary with unstructured data")

    # TIME FOR LOGGING PURPOSES
    end_time = datetime.now()
    total_time = end_time - start_time

    # ---- At these point, if the connection object return an error ( like connection error or other ) we should
    # report these and inform client
    if isinstance(result, dict):
        if result["STATUS"] == "Failure":
            # if status is failure , we are EXPECTING HERE ERROR 4, 3 or 6
            # first Error 4
            if result["ERROR"] == "4":
                # CREATE ERROR OBJECT
                logger_obj = NetworkAutomateLogs(start_time, end_time, total_time, client_info, current.logger,
                                                 user_data_for_logging=user_data_for_logging)
                # CALL METHOD FOR ERROR
                logger_obj.error_netmiko(result)
                # CREATE A JSON LOG
                logger_obj.create_json_log()
                raise InvalidUsage("Bad request!", status_code=512, payload=logger_obj.error_dict)
            # Error 8 FOR NOW THESE ERROR DOESN EXIST YET - LATER WE MAY NEED IT
            # if result["ERROR"] == "8":
            # CREATE ERROR OBJECT
            #    logger_obj = NetworkAutomateLogs(start_time, end_time, total_time, client_info, logger_engine,
            #                                     user_data_for_logging=user_data_for_logging)
            # CALL METHOD FOR ERROR
            #    logger_obj.error_operation_error(result)
            # CREATE A JSON LOG
            #    logger_obj.create_json_log()
            #    raise InvalidUsage("Bad request!", status_code=513, payload=logger_obj.error_dict)

    # Connection to device:Successful. OPERATION SUCCESSFUL  ------ Build log and return interface config to client ----
    # --------- CREATE success LOG -------
    logger_obj = NetworkAutomateLogs(start_time, end_time, total_time, client_info, current.logger,
                                     user_data_for_logging=user_data_for_logging)

    success_dict = {"STATUS": "Success",
                    "MESSAGE": "Check network device cli output to confirm.",
                    "RESULT_OUTPUT_CLI": result
                    }

    final_dict = {"NETWORK AUTOMATE RESPONSE": success_dict}
    # CALL METHOD FOR success messages
    logger_obj.sucess_add_raw_commands(success_dict)
    # CREATE A JSON LOG
    logger_obj.create_json_log()

    # GIVE RESPONSE TO VIEW, for client
    return final_dict
    #return dumps({"message": "hello"})


@api.route("/add_command_raw_not_privileged", methods=["POST"])
def controller_add_raw_commands_not_privileged():
    """
     This view allows a client to send a raw command to a CISCO device in not privileged EXEC mode
    :return: <dict> result of the operation. check documentation for details
    """
    # TODO: convert print screens to app.logger.debug("message")
    print("OUTPUT - Entering function: controller_add_raw_commands_not_privileged")
    # START COUNTING TIME FOR LOGGING PURPOSES
    start_time = datetime.now()

    # GETTING CLIENT INFO, FOR LOGGING
    client_info = get_http_request_info(request)


    # OUTPUT MESSAGES IN DEBUG MODE- ( WE CAN CREATE A DEBUG MODE FOR LOGGING )
    message = "OUTPUT - WEBSERVICE URI: \t'{}'".format(client_info["REQUEST_URI"])
    print(message)
    message = ("OUTPUT - REQUEST_INFORMATION " + str(client_info))
    # ----- --- Below line is just to remember us that we could create a debug mode log with messages like these one.
    # logger_engine.debug(message)
    print("OUTPUT - starting time: {}".format(start_time))
    print(message)

    print("OUTPUT - Let´s request data from client - CHECK IF DATA IS VALID")
    data = request_data(client_info)
    print("OUTPUT - data: ", data)
    if isinstance(data[0], dict):
        if data[0]["STATUS"] == "Failure":
            print("OUTPUT - WE HAVE FOUND AN ERROR......")
            end_time = datetime.now()
            total_time = end_time - start_time
            if data[0]["ERROR"] == "1":
                print("OUTPUT - ERROR 1. LETS RAISE INVALID_USAGE function amd inform client ")
                print("OUTPUT - data", data)
                # CREATE ERROR OBJECT
                logger_obj = NetworkAutomateLogs(start_time, end_time, total_time, client_info, current_app.logger,
                                                 user_data_for_logging= None)
                # CALL METHOD FOR ERROR 1 ( CHECK ERROR-CATALOG.txt for details )
                logger_obj.error_1_json_data(data[0])
                # CREATE A JSON LOG
                logger_obj.create_json_log()
                raise InvalidUsage("Bad request!", status_code=400, payload=logger_obj.error_dict)
            if data[0]["ERROR"] == "2":
                print("OUTPUT - ERROR 2. LETS RAISE INVALID_USAGE function amd inform client ")
                print("OUTPUT - data", data)
                # CREATE ERROR OBJECT
                logger_obj = NetworkAutomateLogs(start_time, end_time, total_time, client_info, current_app.logger,
                                                 user_data_for_logging=data[1])
                # CALL METHOD FOR ERROR 2 ( CHECK ERROR-CATALOG.txt for details
                logger_obj.error_2_fundamental_data_required(data[0])
                # CREATE A JSON LOG
                logger_obj.create_json_log()
                raise InvalidUsage("Bad request!", status_code=400, payload=logger_obj.error_dict)
            if data[0]["ERROR"] == "3":
                print("OUTPUT - ERROR 3. LETS RAISE INVALID_USAGE function amd inform client ")
                print("OUTPUT - data", data)
                # CREATE ERROR OBJECT
                #EXAMPLE HOW DATA SHOULD BE :OUTPUT - \
                # data ({'STATUS': 'Failure', 'ERROR': '3', 'TYPE': 'WEBSERVICE DATA FAILURE', 'MESSAGE':
                # 'Please, send an ip key in your dictionary'}, {'ips': '192.168.7.1'}) ------   -------    is a tuple
                logger_obj = NetworkAutomateLogs(start_time, end_time, total_time, client_info, current_app.logger,
                                                 user_data_for_logging=data[1])
                # CALL METHOD FOR ERROR 3 ( CHECK ERROR-CATALOG.txt for details
                logger_obj.error_webservice_data_failure(data[0])
                # CREATE A JSON LOG
                logger_obj.create_json_log()
                raise InvalidUsage("Bad request!", status_code=400, payload=logger_obj.error_dict)

    print("=" * 79)
    print("OUTPUT - data is OK! ")
    print("OUTPUT - data[0]", data[0])
    print("OUTPUT - data[1]", data[1])
    print("=" * 79)
    # CHECK IF IS PORT
    # MAKE A COPY OF CLIENT DATA for logging purposes
    user_data_for_logging = dict((k, v) for k, v in data[2].items())
    print("OUTPUT - user_data_for_logging:", user_data_for_logging)

    # LETS REMOVE THE KEYS, VLAN_ID AND VLAN_NAME AND STORE THEIR VALUES ON NEW VARIABLES. Construct a dictionary with
    # vlan_id an vlan_name send later. there are a case where client doesn 't send to US vlan_name and we
    # have to process theses kind of behavior
    command_to_send = data[1].pop("command_to_send")
    print("OUTPUT - command_list_to_send: {}".format(command_to_send))

    # CHECK IF CLIENT WANTS A SPECIFIC PORT FOR CONNECTION to device. SET TO NONE if not
    if isinstance(data[1], dict):
        if 'port' in data[1].keys():
            port = data[1].pop("port")
        else:
            port = None

    if data[0]["CONNECTIONS"] == "both":
        #  -------  first try a telnet connection ---------------
        connection = ConnectToDevice(data[1], connection_type="TELNET", port=port)
        # LETS START CONFIGURING
        result = connection.configure_add_raw_commands_not_privileged(command_to_send=command_to_send)

        # result = connection.get_show_run()
        print("OUTPUT - result of telnet connection: ", result)
        print("OUTPUT - type(result): ", type(result))
        print("OUTPUT - result is a list with one dictionary unstructured data")
        result_telnet = result
        end_time = datetime.now()
        total_time = end_time - start_time
        # - ------- At these point we should check if telnet was successful ---------------------
        if isinstance(result_telnet, dict):
            if result_telnet["STATUS"] == "Failure":
                del connection
                print("OUTPUT - Perform a ssh connection because telnet failed ")
                # -- ------ Perform a ssh connection because telnet failed ----------
                connection_new = ConnectToDevice(data[1], connection_type="SSH", port=port)
                # LETS START CONFIGURING
                result = connection_new .configure_add_raw_commands_not_privileged(command_to_send=command_to_send)

                print("OUTPUT - result of ssh connection: ", result)
                print("OUTPUT - type(result): ", type(result))
                print("OUTPUT - result is a list with one dictionary unstructured data")
                result_ssh = result

                if isinstance(result, dict):
                    # ---- Check if ssh connection was successful. if not, inform client of both fails and log
                    if result["STATUS"] == "Failure":
                        # Expecting here to appear error 4 -------- HANDLE ERROR
                        # first handle error 4
                        if result["ERROR"] == "4":
                            # CREATE ERROR OBJECT
                            logger_obj = NetworkAutomateLogs(start_time, end_time, total_time, client_info,
                                                             current_app.logger,
                                                             user_data_for_logging=user_data_for_logging)
                            # CALL METHOD FOR BOTH CONNECTION ERROR
                            logger_obj.error_both_connection_fails("Failed connection to device", result_ssh, result_telnet)
                            # CREATE A JSON LOG
                            logger_obj.create_json_log()
                            print("OUTPUT - result: {}".format(result))
                            raise InvalidUsage("Bad request!", status_code=513, payload=logger_obj.error_dict)
                        # Error 8 FOR NOW THESE ERROR DOESN EXIST YET - LATER WE MAY NEED IT
                        # if result["ERROR"] == "8":
                        # CREATE ERROR OBJECT
                        #    logger_obj = NetworkAutomateLogs(start_time, end_time, total_time, client_info, logger_engine,
                        #                                     user_data_for_logging=user_data_for_logging)
                        # CALL METHOD FOR ERROR
                        #    logger_obj.error_operation_error(result)
                        # CREATE A JSON LOG
                        #    logger_obj.create_json_log()
                        #    raise InvalidUsage("Bad request!", status_code=513, payload=logger_obj.error_dict)

        #  -----  ----- connection to device Successful.   ------ Build log and return info to client ----
        # Connection to device:Successful. OPERATION SUCCESSFUL  ------ Build log and return interface config to client ----
        # --------- CREATE success LOG -------
        logger_obj = NetworkAutomateLogs(start_time, end_time, total_time, client_info, current_app.logger,
                                         user_data_for_logging=user_data_for_logging)
        success_dict = {"STATUS": "Success",
                        "MESSAGE": "Check results. Whenever possible, we will try to output Structured and Unstructured "
                                   "data "
                                   "captured from de Network Device CLI. We have to be careful on what commands we are "
                                   "trying to send, because we are not in privileged mode, and sometimes we are not "
                                   "authorized to run them on the device and the output will be something like: e.g.( "
                                   " ^\n% Invalid input detected at '^' marker.\n )",
                        "STRUCTURED_RESULT": result[0],
                        "UNSTRUCTURED_RESULT": result[1]
                        }

        final_dict = {"NETWORK AUTOMATE RESPONSE": success_dict}
        # CALL METHOD FOR success messages
        logger_obj.sucess_add_raw_commands(success_dict)
        # CREATE A JSON LOG
        logger_obj.create_json_log()

        # GIVE RESPONSE TO VIEW, for client
        return final_dict

    # What differ a ssh or telnet connection is only the device driver used by netmiko, so the first thing we should do,
    # is to know which connection the client want us to perform.
    #  ------   we will pass these choice to the class "ConnectToDevice". ---------------
    if data[0]["CONNECTIONS"] == "telnet":
        connection = ConnectToDevice(data=data[1], connection_type="TELNET", port=port)
    if data[0]["CONNECTIONS"] == "ssh":
        connection = ConnectToDevice(data=data[1], connection_type="SSH", port=port)

    # LETS START CONFIGURING
    result = connection.configure_add_raw_commands_not_privileged(command_to_send=command_to_send)
    print("OUTPUT - configure_add_raw_commands ended ....")
    print("="*79)
    print("OUTPUT - result: ", result)
    print("OUTPUT - type(result): ", type(result))
    # "OUTPUT - result[0] is a list with one dictionary with structured data and a dictionary with unstructured data")

    # TIME FOR LOGGING PURPOSES
    end_time = datetime.now()
    total_time = end_time - start_time

    # ---- At these point, if the connection object return an error ( like connection error or other ) we should
    # report these and inform client
    if isinstance(result, dict):
        if result["STATUS"] == "Failure":
            # if status is failure , we are EXPECTING HERE ERROR 4, 3 or 6
            # first Error 4
            if result["ERROR"] == "4":
                # CREATE ERROR OBJECT
                logger_obj = NetworkAutomateLogs(start_time, end_time, total_time, client_info, current_app.logger,
                                                 user_data_for_logging=user_data_for_logging)
                # CALL METHOD FOR ERROR
                logger_obj. error_netmiko(result)
                # CREATE A JSON LOG
                logger_obj.create_json_log()
                raise InvalidUsage("Bad request!", status_code=512, payload=logger_obj.error_dict)

    # Connection to device: Successful. OPERATION SUCCESSFUL  ------ Build log and return info to client ----
    # --------- CREATE success LOG -------
    logger_obj = NetworkAutomateLogs(start_time, end_time, total_time, client_info, current_app.logger,
                                     user_data_for_logging=user_data_for_logging)

    success_dict = {"STATUS": "Success",
                    "MESSAGE": "Check results. Whenever possible, we will try to output Structured and Unstructured data"
                               " captured from de Network Device CLI. We have to be careful on what commands we are "
                               "trying to send, because we are not in privileged mode, and sometimes we are not "
                               "authorized to run them on the device and the output will be something like: e.g.( "
                               " ^\n% Invalid input detected at '^' marker.\n )",
                    "STRUCTURED_RESULT": result[0],
                    "UNSTRUCTURED_RESULT": result[1]
                    }

    final_dict = {"NETWORK AUTOMATE RESPONSE": success_dict}
    # CALL METHOD FOR success messages
    logger_obj.sucess_add_raw_commands(success_dict)
    # CREATE A JSON LOG
    logger_obj.create_json_log()

    # GIVE RESPONSE TO Client
    return final_dict


# THIS ROUTE SHOULD BE DEACTIVATED ON PRODUCTION. It exists just to force an Internal Server Error.
# Evaluate on how server response to errors, send email functionality and log behaviour
@api.route('/configure_multiple_devices', methods=["POST"])
def controller_multiple_devices():

    """
    # We can put the logic of configure multiple devices at the same time using threading in the other tool.
    :return:
    """
    # devices_list_to_configure = ["192.168.2.100","192.168.2.254"]
    # for device in devices_list_to_configure:
    print("OUTPUT - Entering function: controller_multiple_devices")

    print(this_var_doesnt_exist_and_force_server_error) # FORCE INTERNAL SERVER ERROR. ABOVE CODE SHOULD NOT RUN

    # START COUNTING TIME FOR LOGGING PURPOSES
    start_time = datetime.now()

    # GETTING CLIENT INFO, FOR LOGGING
    client_info = get_http_request_info(request)

    # OUTPUT MESSAGES IN DEBUG MODE- ( WE CAN CREATE A DEBUG MODE FOR LOGGING )
    message = "OUTPUT - WEBSERVICE URI: \t'{}'".format(client_info["REQUEST_URI"])
    print(message)
    message = ("OUTPUT - REQUEST_INFORMATION " + str(client_info))
    # ----- --- Below line is just to remember us that we could create a debug mode log with messages like these one.
    # logger_engine.debug(message)
    print("OUTPUT - starting time: {}".format(start_time))
    print(message)

    # THIS WILL TRIGGER an Internal Server Error
    print("OUTPUT - Let´s request data from client - CHECK IF DATA IS VALID")
    data = request_data(client_info)
    print("OUTPUT - data: ", data)

    # this message will never be returned
    return dumps({"message": "hello"})
