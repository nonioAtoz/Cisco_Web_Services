# !/usr/bin/env python
# -*- encoding: utf-8 -*
# Author: Nuno Moura



import os
import logging
from json import dumps, load
from datetime import datetime
from .request_data import InvalidUsage
from flask import current_app

"""
THESE FILE HAVE all the Classes and  AUXILIARY FUNCTIONS NEEDED FOR THE APP 
"""


def validate_file(path, name):
    """
    This Function test if a certain path for a file and
    a directory exists within the machine
    It receives 2 strings : path and name
    path is the filesystem's path to the directory where file is stored
    name is the filesystem's name of a filename
    :return:<Bolean> True if exist ; False if doesn´t exist
    """
    print("OUTPUT - start validate_file function")
    if path == "":
        fpath = name
    else:
        # construct of the full path for a certain file
        fpath = path + "/" + name

    # this two next variables receive true or false if a file exists
    # file exists - True ::::::::: file not exist - False
    # first one is for the file
    # second one is for the directory
    existencia_ficheiro = os.access(fpath, os.F_OK)
    existencia_dir = os.access(path, os.F_OK)

    # test if a file and directory exists. if not exit the program with
    # the flag 1 code error : which means a error or problem was encontered
    #if (existencia_dir == False):
    #    print("OUTPUT - folder does not exist")
        #return False
    if (existencia_ficheiro == False):
        print("OUTPUT - file does not exist")
        return False
    # FILE AND DIRECTORY EXISTS
    print("OUTPUT - file exists")
    return True


class NetworkAutomateLogs(object):
    """
    Class for managing logs. We can log files:
    .log or .json
    """

    # init method - code inside these method run with the class initialization (when object is created)
    def __init__(self, start_time, end_time, elapsed_time, client_info, logger_engine, user_data_for_logging=None):
        self.start_time = start_time
        self.end_time = end_time
        self.elapsed_time = elapsed_time
        self.client_info = client_info
        self.engine_response = ""
        self.logger_engine = logger_engine
        self.data1 = user_data_for_logging
        # DEFINE ERROR OPERATION DICTIONARY
        self.error_dict = {"STATUS": "Failure",
                           "ERROR": {},
                           "TYPE": {},
                           "MESSAGE": {}
                           }

        # DEFINE SUCCESS OPERATION DICTIONARY
        self.success_dict = {"STATUS": "Success",
                             "MESSAGE": {},
                             "RESULT": ""
                             }

        # DEFINE DICTIONARY FOR JSON LOGS
        self.json_log_dict = {
            "NETWORK_AUTOMATE_RESPONSE": self.engine_response,
            "DATA_SENT_OFF_BY_CLIENT": None,
            'TIME_REQUEST': str(self.start_time),
            'TIME_RESPONSE': str(self.end_time),
            "TIME_ELAPSED": str(self.elapsed_time),
            "ENVIRONMENT_DATA": self.client_info,

        }
        print("OUTPUT - CLASS logger")

    def error_1_json_data(self, error_data):
        """
        These is the method for our engine ERROR 1
        It will fill with data, the empty class dictionary "error_dict". (attribute of object ) .
        It also assign data to a key in the class dictionary "json_log_dict"
        :return: None
        """
        print("OUTPUT - error_1_json_data 'method' --> class NetworkAutomateLogs")

        self.error_dict['ERROR'] = str(error_data["ERROR"])
        self.error_dict['TYPE'] = error_data["TYPE"]
        self.error_dict['MESSAGE'] = error_data["MESSAGE"]
        # put the error dict in our json log dict
        self.json_log_dict['NETWORK_AUTOMATE_RESPONSE'] = self.error_dict
        # write log message
        self.logger_engine.info(self.json_log_dict)
        return

    def error_2_fundamental_data_required(self, data_error):
        """
        It will fill with data the empty class dictionary "error_dict". (attribute of object ) .
        It also assign data to a key in the class dictionary "json_log_dict"
        :return: None
        """
        print("OUTPUT - error2 'method' - class NetworkAutomateLogs")

        self.error_dict['ERROR'] = str(data_error["ERROR"])
        self.error_dict['TYPE'] = data_error["TYPE"]
        self.error_dict['MESSAGE'] = data_error["MESSAGE"]
        # put the error dict in our json log dict
        self.json_log_dict['NETWORK_AUTOMATE_RESPONSE'] = self.error_dict
        self.json_log_dict['DATA_SENT_OFF_BY_CLIENT'] = self.data1

        # write log message
        self.logger_engine.info(self.json_log_dict)
        return

    def error_netmiko(self, netmiko_error):
        """
        :param netmiko_error:<dict> dictionary with error
        :return: None
        """
        print("OUTPUT - error4 'method' - class NetworkAutomateLogs")
        self.error_dict['ERROR'] = str(netmiko_error["ERROR"])
        self.error_dict['TYPE'] = str(netmiko_error['TYPE'])
        message = netmiko_error["MESSAGE"]
        # convert message to string and eliminate the characteres "\r\n" present in messages
        message = str(message)
        message = message.replace("\r\n", " ")
        #message = message.encode("utf-8")
        self.error_dict['MESSAGE'] = str(message)

        # put the error dict in our json log dict
        self.json_log_dict['NETWORK_AUTOMATE_RESPONSE'] = self.error_dict
        self.json_log_dict['DATA_SENT_OFF_BY_CLIENT'] = self.data1

        # write log message
        self.logger_engine.info(self.json_log_dict)

    def error_both_connection_fails(self, message, ssh_error, telnet_error):
        """
        These is the method for our engine ERROR 2
        It will fill with data the empty class dictionary "error_dict". (attribute of object ) .
        It also assign data to a key in the class dictionary " json_log_dict

        :param message:
        :return: None
        """
        self.error_dict['ERROR'] = str(5)
        self.error_dict['TYPE'] = str("BOTH CONNECTION FAIL")
        # convert message to string
        message = str(message)
        message = message.replace("\r\n", " ")
        self.error_dict['MESSAGE'] = str(message)

        # put the error dict in our json log dict
        self.json_log_dict['NETWORK_AUTOMATE_RESPONSE'] = self.error_dict
        self.json_log_dict['NETWORK_AUTOMATE_RESPONSE']['SSH FAILURE'] = ssh_error
        self.json_log_dict['NETWORK_AUTOMATE_RESPONSE']['TELNET FAILURE'] = telnet_error
        self.json_log_dict['DATA_SENT_OFF_BY_CLIENT'] = self.data1
        # write log message
        self.logger_engine.info(self.json_log_dict)

    def error_webservice_data_failure(self, error_webservice_data):
        """
        These error is used when key and values present in json data sent off by client are not OK.
        These keys are fundamental!
        Keys are:
            - port ( We expect from 1 to 65535)
            - type ( 'ssh' or 'telnet')
         Note: WE HAVE A Function named 'validate_user_data' that will process the validation for these keys and if
         it finds an error will send what error was detected (check validate_user_data for details)
        :param message: <string> A error message sent by validate_user_data
        :return:
        """

        self.error_dict['ERROR'] = str(error_webservice_data['ERROR'])
        self.error_dict['TYPE'] = str(error_webservice_data['TYPE'])
        self.error_dict['MESSAGE'] = str(error_webservice_data['MESSAGE'])
        # put the error dict in our json log dict
        self.json_log_dict['NETWORK_AUTOMATE_RESPONSE'] = self.error_dict
        self.json_log_dict['DATA_SENT_OFF_BY_CLIENT'] = self.data1

        # write log message
        self.logger_engine.info(self.json_log_dict)

    def error_operation_error(self, operation_error):
        """
        These error is used when key and values present in json data sent off by client are not OK.
        These keys are fundamental!
        Keys are:
            - port ( We expect from 1 to 65535)
            - type ( 'ssh' or 'telnet')
         Note: WE HAVE A Function named 'validate_user_data' that will process the validation for these keys and if
         it finds an error will send what error was detected (check validate_user_data for details)
        :param message: <string> A error message sent by validate_user_data
        :return:
        """
        self.error_dict['STATUS'] = str(operation_error['STATUS'])
        self.error_dict['ERROR'] = str(operation_error['ERROR'])
        self.error_dict['TYPE'] = str(operation_error['TYPE'])
        self.error_dict['MESSAGE'] = str(operation_error['MESSAGE'])
        # put the error dict in our json log dict
        self.json_log_dict['NETWORK_AUTOMATE_RESPONSE'] = self.error_dict
        self.json_log_dict['DATA_SENT_OFF_BY_CLIENT'] = self.data1

        # write log message
        self.logger_engine.info(self.json_log_dict)

    def error_405(self, error_data):
        """
        These is the method for our engine ERROR 1
        It will fill with data, the empty class dictionary "error_dict". (attribute of object ) .
        It also assign data to a key in the class dictionary "json_log_dict"
        :return: None
        """
        print("OUTPUT - error_1_json_data 'method' --> class NetworkAutomateLogs")

        self.error_dict['ERROR'] = str(error_data["ERROR"])
        self.error_dict['TYPE'] = error_data["TYPE"]
        self.error_dict['MESSAGE'] = error_data["MESSAGE"]
        # put the error dict in our json log dict
        self.json_log_dict['NETWORK_AUTOMATE_RESPONSE'] = self.error_dict
        # write log message
        self.logger_engine.error(self.json_log_dict)
        return

    def http_errors_met(self, data_error):
        """
        make logs on http errors 400 ,405 etc
        :param data_error:
        :return:
        """
        print("OUTPUT -  http_errors_met --> class NetworkAutomateLogs")
        self.error_dict['ERROR'] = str(data_error["code"])
        self.error_dict['TYPE'] = data_error["name"]
        self.error_dict['MESSAGE'] = data_error["description"]
        # put the error dict in our json log dict
        self.json_log_dict['NETWORK_AUTOMATE_RESPONSE'] = self.error_dict
        #self.json_log_dict['DATA_SENT_OFF_BY_CLIENT'] = self.data1
        # write log message
        self.logger_engine.info(self.json_log_dict)
        return

    def create_json_log(self):
        """
        WRITE THE JSON LOG
        :param entry: <dict> new entry for json file
        :return:
        """
        #fname = "LOGS/NetworkAutomateJsonLog.json"  # default expected
        # LETS GET THE FILE NAME AND PATH FOR OUR JSON LOG FILE. fname will be the fullpath as the example in above line
        folder = current_app.config["LOG_FOLDER"]
        fname = folder + "/" + current_app.config["JSON_LOG_FILE"]

        entry = self.json_log_dict
        a = []
        # file does not exist so lets write to file
        if validate_file("", fname) == False:
            a.append(entry)
            with open(fname, mode='w') as f:
                f.write(dumps(a, indent=4))
        else:
            # file already exists. load data, append new entry, write to file
            with open(fname) as feedsjson:
                feeds = load(feedsjson)

            feeds.append(entry)
            with open(fname, mode='w') as f:
                f.write(dumps(feeds, indent=4))

    def sucess_log(self, message, results=None):
        """

        :param message: <string> message to log to file
        :param results: <any data type>
        :return: nothing
        """
        # DEFINE SUCCESS OPERATION DICTIONARY
        self.success_dict['MESSAGE'] = str(message)
        """

        :return:
        """
        self.success_dict = {"STATUS": "Success",
                             "MESSAGE": message,
                             "RESULT": results
                             }

        # put the error dict in our json log dict
        self.json_log_dict['NETWORK_AUTOMATE_RESPONSE'] = self.success_dict
        self.json_log_dict['DATA_SENT_OFF_BY_CLIENT'] = self.data1

        # write log message
        self.logger_engine.info(self.json_log_dict)

    def sucess_log_two_results(self, message, results=None):
        """
        These method is for logging for services that have a different output result.
        ( structured data and unstructered data)
        :param message: <string> message to log to file
        :param results: <list>
        result[0] - structured data
        result[1] - unstructured data
        :return: None
        """
        # DEFINE SUCCESS OPERATION DICTIONARY
        self.success_dict['MESSAGE'] = str(message)
        """
        :return:
        """
        self.success_dict = {"STATUS": "Success",
                             "MESSAGE": message,
                             "RESULT_STRUCTURED_DATA": results[0],
                             "RESULT_UNSTRUCTURED_DATA": results[1]
                             }

        # put the error dict in our json log dict
        self.json_log_dict['NETWORK_AUTOMATE_RESPONSE'] = self.success_dict
        self.json_log_dict['DATA_SENT_OFF_BY_CLIENT'] = self.data1

        # write log message
        self.logger_engine.info(self.json_log_dict)

    def sucess_add_raw_commands(self, success_dict):
        """
        These method is for logging for services add_waw_commands

        :param results: <list> we are expecting a list with 2 or 3 elements

        success_dict<dict> stuctured data dict to output

         ----------   WE will log operation information status and more in files "network_automate.log" and "json.JSON"

        :return: None
        """
        self.success_dict = success_dict
        # DEFINE SUCCESS OPERATION DICTIONARY
        #self.success_dict['MESSAGE'] = str(message)

        #self.success_dict = {"STATUS": "Success",
        #                     "MESSAGE": message,
        #                     "RESULT_STRUCTURED_DATA": results[0],
        #                     "RESULT_UNSTRUCTURED_DATA": results[1]
        #                     }
        # put the error dict in our json log dict
        self.json_log_dict['NETWORK_AUTOMATE_RESPONSE'] = self.success_dict
        self.json_log_dict['DATA_SENT_OFF_BY_CLIENT'] = self.data1

        # write log message
        self.logger_engine.info(self.json_log_dict)
