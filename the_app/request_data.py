# !/usr/bin/env python
# -*- encoding: utf-8 -*
import os
import logging
from json import dumps
from flask import jsonify
from re import compile
from datetime import datetime
from flask import request
from flask import current_app

"""
THESE FILE HAVE all the Classes and  AUXILIARY FUNCTIONS NEEDED FOR THE APP 
"""


class InvalidUsage(Exception):
    status_code = 400
    """
    WE USE THIS FUNCTION TO RAISE ERROR AND RETURN THE ERROR TO CLIENT. 
    We ALSo manipulate the http response (content type, messages and status code)
    
    
    Check website for details:
    https://flask.palletsprojects.com/en/1.1.x/patterns/apierrors/
    """
    def __init__(self, message=None, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        print("OUTPUT - Inside to_dict method - Class InvalidUsage")
        rv1 = dict(self.payload or ())
        # SEND RESPONSE TO CLIENT
        print("OUPTUT - Inform client and delivery The NETWORK_AUTOMATE_RESPONSE error message ..... ")
        for_client_rv2 = {"NETWORK_AUTOMATE_RESPONSE": rv1}
        print("OUTPUT - NETWORK_AUTOMATE_RESPONSE: ", str(for_client_rv2))
        return for_client_rv2


# A simple logger without file rotation. Currently not in use.
def setup_logger(name, log_file, level=logging.INFO):
    """
    Function to setup as many loggers as we want
    # Comments:
        # IF WE WANT TO RUN IN DEBUG MODE to log all messages
            # CHANGE level using Formatter ( above ) >>> level=logging.DEBUG
        # IF WE WANTO TO RUN AND LOG JUST IMPORTANT MESSAGES
            # CHANGE level using Formatter ( above ) >>> level=logging.INFO
    """
    # CHECK Logging documentation for details
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


def validate_ipv4(ip):
    """
    This function checks if a string is a valid ipv4 address
    :param ip: string that contains a ipv4 address
    :return: 1 if ip is a valid ip
             0 if ip is not ipv4 valid ip
    """

    print("OUTPUT - EXECUTING FUNCTION: 'validate_ipv4")
    ipv4_address = compile('^(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|'
                              '25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]''{2}|'
                              '2[0-4][0-9]|25[0-5])$')
    result = ipv4_address.match(ip)
    if ip is "255.255.255.255":
        print("OUTPUT - Invalid ipv4. Check your ip!")
        return False
    if result:
        print("OUTPUT - Valid ipv4. OK! ")
        return True
    else:
        print("OUTPUT - Invalid ipv4. Check your ip!")
        return False
    #TODO: we can have a list of forbiden ips
    # and to not allow an ip where the last octet is 255

    # MORE DETAILS -----------------------------------------------------------------
    # https://gist.github.com/mnordhoff/2213179
    # Python regular expressions for IPv4 and IPv6 addresses and URI-references,
    # based on RFC 3986's ABNF.
    # ipv4_address and ipv6_address are self-explanatory.


def get_http_request_info(request):
    """
    This function will tell important information about a client that make a request to
    a Flask  web service
    This may be useful for our logSystem
    If we need more info, read the docs available  for "request"
    :param request: http request
    :return: <dictionary> almost all flask environment variables of the HTTP request
    """
    current_app.logger.debug("OUTPUT - Entering Function:  get_http_request_info")

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
        'REQUEST_HEADERS': request_headers
    }
    current_app.logger.debug("OUTPUT - EXECUTING FUNCTION:  get_http_request_info")
    return environment_data


def check_if_is_json():
    current_app.logger.debug("OUTPUT - Starting function check_if_is_json")
    success_dict = {"STATUS": "Success"}

    # CHECK IF CONTENT IS 'application/json' - (for cases that clients try to send us xml ou html or javascript or ...)
    if request.headers['Content-Type'] != 'application/json':
        current_app.logger.debug("OUTPUT - FOUND ERROR ON DATA - 'MESSAGE': We could not continue. Please, s"
                                 "end us JSON DATA.")
        error_dict = {"STATUS": "Failure", "MESSAGE": "We could not continue. Please, send us JSON DATA.",
                      "TYPE": "JSON ERROR", "ERROR": "1"}
        return error_dict

    # LOAD JSON DATA FROM CLIENT
    try:
        data = request.json
    # Catch exceptions - Client doesn't send us json data or json dictionary is not well formatted"
    # For specific dictionary keys and values present in the data dictionary  we will check them later
        current_app.logger.debug("OUTPUT - Data is JSON. Data OK - exist and 'deliver success_dict' and 'data'")
        return success_dict, data
    except Exception as error:
        current_app.logger.debug("OUTPUT - ERROR FOUND - EXCEPTION in function 'check_if_is_json'")
        error_dict = {"STATUS": "Failure",
                      "MESSAGE": "We could not process your data. Check you dictionary. Send us JSON DATA.",
                      "TYPE": "JSON ERROR", "ERROR": "1"}
        return error_dict


def validate_fundamental_parameters(data):
    """
    ...
    :param data: <dictionary> sent by user
    :return: <list> with 4 items
        <list>[item1 <string>|<dictionary, item2 <string>|<dictionary, item3<list>, item4 <dictionary>]


        item1: <string> we will export a string value: it can be one of these three strings
                "telnet"
                "ssh"
                "both"
        <item2> and <item3> are <dictionaries> or empty strings
        when an error occur they will be empty strings
        when client doesn´t know what type of connection he wants we will export 2 <dictionarys> with data for netmiko
            - One for telnet use
            - and the other one for ssh connections
        other case is when client wants a specific type of connection. For example telnet. we will  only export
        the first one and the second will be an empty string

        item3:<list> with two items  <list>[item0 <string>, item1<string>]
            item0: <string> is "Sucess" or "ERROR"-  it represents the state
            item1: <string> is a message describing what is happening in our code
                                        EX item3 [ "ERROR", "message"] or ["Sucess", "message"]
                                        It will be useful for logs
        item4: is optional -<dictionary> WE only output this when a error is found.
                                        We export a dictionary {"ERROR": "message"}
                                        It will be usefull for exporting structured data from our webservices
        """

    current_app.logger.debug("OUTPUT - Starting function: 'validate_fundamental_parameters'")
    # CALL (STANDARD FAILURE DICTIONARY) AND SET VALUES FOR THIS OPERATION ERROR
    error_dictionary = {}
    error_dictionary["ERROR"] = "2"
    error_dictionary["TYPE"] = "WEBSERVICE FUNDAMENTAL DATA REQUIRED"
    error_dictionary["STATUS"] = "Failure"
    success_dictionary = {"STATUS": "Success",
                          "CONNECTIONS": {}
                          }
    # for security check if client inject the Key "STATUS" and if so, remove it from data dictionary
    #if type(data) == dict:
    #    if data["STATUS"]:
    #        del data["STATUS"]  # Removes specific element in a dictionary

    # WE ARE GOING TO PERFORM A SERIES OF CHECKS ON DATA SENT BY USER
    # DOESN'T EXIST PORT AND TYPE KEYS
    # Create a new object dictionary -its a copy of user data. it useful for logging
    user_data = dict((k, v) for k, v in data.items())
    print("OUTPUT - ENTERING function :'validate_fundamental_parameters'")
    if not 'port' in user_data.keys() and not 'type' in user_data.keys():
        success_dictionary["CONNECTIONS"] = "both"
        return success_dictionary, user_data
    #if "port" in data.keys():
    #    if isinstance(data['port'], int):
    #        if user_data['port'] < 1:
    #            error_dictionary["MESSAGE"] = "Please, send a number between 1 and 65535 for 'port' key"
    #            return error_dictionary
    #        if user_data['port'] > 65535:
    #            error_dictionary["MESSAGE"] = "Please, send a number between 1 and 65535 for 'port' key"
    #            return error_dictionary
    # CHECK IF "port" KEY EXISTS IN DATA
    if 'port' in user_data.keys():
        if isinstance(data['port'], int):
            if user_data['port'] < 1:
                error_dictionary["MESSAGE"] = "Please, send a number between 1 and 65535 for 'port' key"
                return error_dictionary
            if user_data['port'] > 65535:
                error_dictionary["MESSAGE"] = "Please, send a number between 1 and 65535 for 'port' key"
                return error_dictionary

        # CHECK IF "port" KEY EXISTS IN DATA  ANF IF IS A VALID TYPE OF DATA. WE ARE EXPECTING <INT> NUMBER.
        if not isinstance(user_data['port'], int):
            error_dictionary["MESSAGE"] = "Please, send a [int] number for 'port' key"
            return error_dictionary
        # WE could also check - if integer is in a valid interval of numbers (1-65536)
        # WE DIDNT CHECK FOR LARGE  NUMBERS LIKE 3954662342423435
        # AT THIS POINT, A "port" KEY EXISTS, AND IS VALID -
        # CHECK IF  type key exists  in data and THE VALUE IS IN A CORRECT DATA TYPE. WE ARE EXPECTING <STRING>.
        if 'type' in user_data.keys():
            if not isinstance(user_data['type'], str):
                error_dictionary["MESSAGE"] = "Please, send a [string] value for 'type' key."
                return error_dictionary
            # AT THIS POINT EXISTS "port" AND "type" AND ARE WELL FORMATED
            # we ARE EXPECTING FOR TYPE A STRING "telnet" OR "ssh" -TELLING US THE TYPE OF CONNECTION CLIENT WANTS
            # NOW LETS CONSTRUCT OUR DICIONARY DATA FOR OUTPUT. NETMIKO EXPECT A "device_type" KEY AND VALUE
            # FOR CISCO SSH - "devic_type" : "cisco_ios"
            # FOR CISCO TELNET -  "device_type": "cisco_ios_telnet"
            # IF CLIENT SEND AS A STRING FOR TYPE THAT IS NOT "telnet" OR "ssh" EXIT AND INFORM CLIENT FOR BAD REQUEST
            else:
                print("OUTPUT - 'port'- EXISTS. 'type' - Exists - LETS SET 'device_type")
                if user_data['type'] == "telnet":
                    del user_data['type']  # Removes specific element in a dictionary
                    # return "telnet", data, "", ["Success", " outputting client data "]
                    success_dictionary["MESSAGE"] = "outputting client data"
                    success_dictionary["CONNECTIONS"] = "telnet"
                    return success_dictionary, user_data
                elif user_data['type'] == "ssh":
                    del user_data['type']  # Removes specific element in a dictionary
                    success_dictionary["MESSAGE"] = "outputting client data"
                    success_dictionary["CONNECTIONS"] = "ssh"
                    return success_dictionary, user_data
                else:
                    error_dictionary["MESSAGE"] = "WE are expecting 'ssh or 'telnet' for 'type' key."
                    return error_dictionary

        # AT THIS POINT, A "port" key EXISTS IN DATA, BUT NO "type" key
        # LETS SET DEFAULTS. WE ARE GOING TO EXPORT 2 DICTIONARIES. ONE FOR SSH CONNECTIONS AND THE OTHER FOR TELNET
        #
        else:
            # print ( "[OUTPUT: 'port' EXISTS! NO 'type' EXISTS. LETS SET DEFAULTS FOR TYPE")
            # CREATING 2 DICTIONARIES FOR TELNET AND SSH
            success_dictionary["CONNECTIONS"] = "both"
            return success_dictionary, user_data

    # AT THIS POINT NO "port" KEY EXISTS
    else:
        # print("[OUTPUT: Nao existe porto")
        # CHECK IF "type" EXISTS IN DATA
        if 'type' in user_data.keys():
            print("OUTPUT - there is 'type' on client data")
            # CHECK IF THE VALUE FOR "type" IS A VALID DATA TYPE. WE ARE EXPECTING A <STRING>
            # IF NOT EXIT AND INFORM CLIENT
            if not isinstance(user_data['type'], str):
                print("OUTPUT - data['type'] is not a string")
                error_dictionary["MESSAGE"] = "Please, send a [string] value for 'type' key."
                return error_dictionary
            # AT THIS POINT "port" DOESN'T EXISTS . "type" EXISTS AND IS WELL FORMATTED
            # LET'S BUIlD OUR DATA FOR OUTPUT. CHECK WHAT TYPE OF CONNECTION CLIENT WANTS AND SET "port" DEFAULTS
            # DEFAULTS SSH CONNECTION - PORT 22
            # DEFAULTS TELNET CONNECTION - PORT 23
            # IF type IS NOT "ssh" OR "telnet" EXIT AND INFORM CLIENT THAT WE DON´T KNOW WHAT HE WANTS
            print("OUTPUT - 'port' doens't exist. Check for 'type' and 'set device_type'")
            if user_data['type'] == "telnet":
                del user_data['type']
                # return "telnet", data, "", ["Success", "Outputting Telnet data"]
                success_dictionary["CONNECTIONS"] = "telnet"
                return success_dictionary, user_data

            elif user_data['type'] == "ssh":
                del user_data['type']
                success_dictionary["CONNECTIONS"] = "ssh"
                return success_dictionary, user_data
            else:
                error_dictionary["MESSAGE"] = "WE are expecting 'ssh or 'telnet' for type key."
                return error_dictionary


def request_data(client_info):
    current_app.logger.debug("OUTPUT - Starting function request_data...")
    print("OUTPUT - STARTING function request_data...")
    data = check_if_is_json()
    # data = success_dict, data       OR data = error_dict
    print("OUTPUT - data {}".format(data))
    if isinstance(data, dict):
        if data["STATUS"] == "Failure":
            print("OUTPUT - BUILD LOG AND RETURN INFO TO CLIENT")
            return data, None
        else:
            pass

    # At these point, data = success_dict, data
    # old_data is raw data sent to us (LOAD JSON)
    old_data = data[1]
    print("OUTPUT - old_data: ", data[1])

    data = validate_fundamental_parameters(data[1])
    # now data could be: data = success_dictionary, data     OR data = error_dictionary

    print("OUTPUT - data: ", data)
    if isinstance(data, dict):
        if data["STATUS"] == "Failure":
            print(" BUILD LOG AND RETURN INFO TO CLIENT")
            return data, old_data
        else:
            pass

    print("OUTPUT - data[0]: {}".format(data[0]))
    print("OUTPUT - data[1]: {}".format(data[1]))

    result = check_webservice_data(data=data[1], client_info=client_info)
    if result is "ok":
        print("OUTPUT - check_webservice_data: OK")
        print("OUTPUT - data[0]: {}".format(data[0]))
        print("OUTPUT - data[1]: {}".format(data[1]))
        print("OUTPUT - result:", result)
        # OUTPUT - data[0]: {'STATUS': 'Success', 'CONNECTIONS': 'telnet'}
        # OUTPUT - data[1]: {'ip': '192.168.7.100'}
        print("OUTPUT: Returning data[0] and data[1]")
        return data[0], data[1], old_data
    else:
        # result is error dictionary. data[1] ia data sent off by client
        print("OUTPUT: Returning result and data[1]")
        return result, data[1]


def check_webservice_data(data, client_info):
    """
    THIS FUNCTION WILL CHECK IF SOME KEYS ARE PRESENT IN A DICTIONARY AND THEIR VALUES ARE IN
    A CORRECT FORMAT (AS WE EXPECT TO BE) . IT CAN CHECK WHICH WEB SERVICE is REQUESTED AND GIVE THE
    RIGHT ANSWER ACCORDINGLY .

    AS AN EXAMPLE, IF THE WEBSERVICE IS: /add_interface_description -
        WE ARE EXPECTING FOR THESE SERVICE, AN INTERFACE AND AN INTERFACE DESCRIPTION, SO WE WILL VALIDATE THESE KEYS
    A DIFFERENT EXAMPLE, IS THE CASE WHERE WEBSERVICE IS: /add_vlan
        WE ARE EXPECTING FOR THESE SERVICE, A VLAN_ID AND A VLAN_NAME, SO WE WILL VALIDATE THESE KEYS

    WHEN KEYS ARE AS EXPECTED TO BE, WE WILL EXPORT A <string> "Ok"

    WHEN KEYS ARE IN A WAY AS WE DON'T EXPECT THEM TO BE, (WE WILL EXPORT A DICTIONARY WITH data
    ERROR_DICT = { "TYPE": <string>,
                   "MESSAGE": <string>,
                   "STATUS": <string>,
                   "ERROR": <string>}

    :param data: <dictionary>
    :param client_info: <list> typically this is will tell important information about a client that make a request to
                            -   http_request
    :return:<str>"ok" or a <dictionary> error_dict

    """
    current_app.logger.debug("OUTPUT - ENTERING FUNCTION : check_webservice_data")
    print ("OUTPUT - EXECUTING FUNCTION : check_webservice_data")
    print("OUTPUT - data : {}".format(data))

    success_dict = {"STATUS": "Success", "MESSAGE": "", "RESULT": ""}
    error_dict = {"STATUS": "Failure",
                  "ERROR": "3",
                  "TYPE": "WEBSERVICE DATA REQUIRED",
                  "MESSAGE": {}
                  }

    # CHECK IF THERE IS ANY KEY PRESENT IN THE DATA SENT OFF BY CLIENT
    # CASE THAT IS EMPTY: HAVE NO KEYS AND VALUES
    if len(data) == 0:
        error_dict["MESSAGE"] = "You are full of nothing. we need you to send us data. Check documentation."
        return error_dict

    # THIS IS  FOR ALL WEB SERVICES, "/" .
    if client_info["REQUEST_URI"] != '/':
        # case:
        # VALIDATE IF AN IP KEY IS PRESENT IN DATA AND IF IT IS, check if it is IN a EXPECTED FORMAT <STRING>.
        # IF NOT EXIT --> return error dictionary data
        if not 'ip' in data.keys():
            error_dict["MESSAGE"] = "Please, send an ip key in your dictionary"
            return error_dict
        if not isinstance(data['ip'], str):
            error_dict["MESSAGE"] = "Please, send a [str] number for 'ip' key"
            return error_dict
        # CALL FUNCTION AND  VALIDATE IF IP IS CORRECT, IF NOT INFORM CLIENT
        if validate_ipv4(data['ip']) is False:
            error_dict["MESSAGE"] = "Invalid ipv4 ip! Please, check you ip."
            return error_dict
        else:
            print("OUTPUT - Valid ipv4. OK!")
    else:
        # CASE IN MULTIPLE_DEVICES # IF WE HAVE A SERVICE THAT RECEIVE A LIST OF IPS TO CONFIGURE
        pass
    ####################################################################################################################
    # A CORNER SITUATION.
    ####################################################################################################################
    # RATIONALE: PROBLEM OCCUR WHEN WE ARE PASSING TO THE REQUEST a double "/"
    # EXAMPLE - request in POSTMAN -->          127.0.0.1//add_command_raw_not_privileged
    #
    # FLASK see this:
    # 'RAW_URI': '//add_command_raw_not_privileged',
    # but it not raises a page not found, HTTP error 404
    #
    # for flask :
    # 'RAW_URI': '/add_command_raw_not_privileged' is the same as 'RAW_URI': '//add_command_raw_not_privileged', and
    # FLASK will continue with the request. In a case where we are expecting a key and value pair, this pair may
    # not be verified and it will raise an error.
    # To prevent this we will check for second letter of the RAW_URI. IN A GOOD REQUEST(as we expect it to be), the s
    # second letter should never be a "/"

    if client_info["REQUEST_URI"][1] == "/":
        error_dict["MESSAGE"] = "Please, Don't send more than one backslash."
        return error_dict

    ####################################################################################################################
    # FOR WEBSERVICE SPECIFIC CHECK KEY AND VALUES SENT OFF BT CLIENT -
    ####################################################################################################################

    # FOR WEBSERVICE : /add_command_raw
    # FOR THIS SERVICE, WE EXPECT command_to_send
    # "/add_command_raw"
    if client_info["REQUEST_URI"] == '/add_command_raw':
        # CHECK IF command_to_send is present in our data and it is well formatted
        print("OUTPUT - CHECKING WEBSERVICE DATA for view:  /add_command_raw")
        if not 'command_to_send' in data.keys():
            error_dict["MESSAGE"] = "Please, send 'command_to_send' key in your dictionary"
            return error_dict
        if not isinstance(data['command_to_send'], str):
            error_dict["MESSAGE"] = "Please, send a string [str] for 'command_to_send' key"
            return error_dict
        if data['command_to_send'].isspace():
            error_dict["MESSAGE"] = "Please, send something for 'command_to_send' key. Your string is full of nothing"
            return error_dict

    # FOR WEBSERVICE : /add_command_raw_not_privileged
    # FOR THIS SERVICE, WE EXPECT command_to_send
    # /add_command_raw_not_privileged
    if client_info["REQUEST_URI"] == '/add_command_raw_not_privileged':
        # CHECK IF command_to_send is present in our data and it is well formatted
        print("OUTPUT - CHECKING WEBSERVICE DATA for view:  /add_command_raw")
        if not 'command_to_send' in data.keys():
            error_dict["MESSAGE"] = "Please, send 'command_to_send' key in your dictionary"
            return error_dict
        if not isinstance(data['command_to_send'], str):
            error_dict["MESSAGE"] = "Please, send a string [str] for 'command_to_send' key"
            return error_dict
        if data['command_to_send'].isspace():
            error_dict[
                "MESSAGE"] = "Please, send something for 'command_to_send' key. Your string is full of nothing"
            return error_dict

    # FOR SPECIFIC WEBSERVICE, CHECK KEY AND VALUES SENT OFF By CLIENT - for this service we expect a "command_list"
    # FOR WEBSERVICE : /add_list_of_commands
    if client_info["REQUEST_URI"] == '/add_list_of_commands':
        # CHECK IF 'MODE' AND 'INTERFACE' KEYS ARE PRESENT IN OUR DATA AND WELL WELL FORMATTED
        print("OUTPUT - CHECKING WEBSERVICE DATA for view:  /add_list_of_commands")
        if not 'commands_list' in data.keys():
            print("OUTPUT - CHECKING WEBSERVICE DATA - is there any list of commands ?")
            error_dict["MESSAGE"] = "Please, send 'command_list' key in your dictionary. Example: It can be " \
                                    "'command_list': ['vlan 99','name Vlan_for_admin', 'do show vlan brief']. " \
                                    "It´s mandatory. Check specifications for more details."
            return error_dict
        if not isinstance(data['commands_list'], list):
            print("OUTPUT- HERE in --> isinstance(data['commands_list'], list)")
            error_dict["MESSAGE"] = "Please, send a <list> with Cisco IOS commands <strings> " \
                                          "Example: It can be " \
                                          "'command_list': ['vlan 99','name Vlan_for_admin','do show vlan brief']. " \
                                          "It´s mandatory. Check specifications for more details."
            return error_dict

        for item in data["commands_list"]:
            print("------------------")
            print("OUTPUT - item: {}".format(item))
            print("OUTPUT - type(item): {}".format(type(item)))
            print("--------------------")
            if isinstance(item, str):
                pass
            else:
                print("OUTPUT- FOUND A ERROR in : a command present in the command list")
                error_dict["MESSAGE"] = "Please, send a <string> in the commands_list " \
                                        "Example: It can be " \
                                        "'command_list': ['vlan 99','name Vlan_for_admin','do show vlan brief']. " \
                                        "It´s mandatory. Check specifications for more details."
                return error_dict
    # NO ERRORS FOUND AT THIS POINT . return string "ok"
    print("OUTPUT - EXECUTING FUNCTION : check_webservice_data: return 'ok'" )
    return "ok"



