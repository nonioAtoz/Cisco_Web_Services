# !/usr/bin/env python
# -*- encoding: utf-8 -*
# Autor: Nuno Moura
# Coordenação: Alexandre Santos, Pedro Vapi

from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
from netmiko import SSHDetect

from flask import current_app


def guess_device(ip, port=None):
    #device_credentials = {"device_username": "cisco",
    #                      "device_password": "cisco",
    #                      "device_secret": "password"  # for entering in (enable) exec mode on cisco device.
    #                      }
    device_credentials = {"device_username": current_app.config["DEVICE_USERNAME"],
                          "device_password": current_app.config["DEVICE_PASSWORD"],
                          "device_secret": current_app.config["DEVICE_SECRET"]
                          }

    # (STANDARD FAILURE DICTIONARY) AND SET VALUES FOR THIS OPERATION ERROR
    error_dictionary = {"STATUS": "Failure",
                             "ERROR": "4",
                             "TYPE": {},
                             "MESSAGE": {}
                             }
    try:
        if port is None:
            port = 22
        guesser = SSHDetect(device_type="autodetect",
                                          ip=ip,
                                          username=device_credentials["device_username"],
                                          password=device_credentials["device_password"],
                                          secret=device_credentials["device_secret"],
                                          port=port)
        best_match = guesser.autodetect()
        print("OUTPUT _INSIDE - guess_device function")
        print("OUTPUT - best_match is: ", best_match )  # Name of the best device_type to use further
        print("OUTPUT - Dictionary of the whole matching results: ", guesser.potential_matches)  # Dictionary of the whole matching result
        return best_match
    except AuthenticationException as e:
        error_dictionary["STATUS"] = "Failure"
        error_dictionary["TYPE"] = "AuthenticationException"
        error_dictionary["MESSAGE"] = str(e)
        # SEND ERROR MESSAGE TO CLIENT
        return error_dictionary
    except NetMikoTimeoutException as e:
        error_dictionary["STATUS"] = "Failure"
        error_dictionary["TYPE"] = "NetMikoTimeoutException"
        error_dictionary["MESSAGE"] = str(e)
        # SEND ERROR MESSAGE TO CLIENT
        return error_dictionary
    except SSHException as e:
        error_dictionary["STATUS"] = "Failure"
        error_dictionary["TYPE"] = "SSH_exception"
        if "Error reading SSH protocol banner" in str(e):
            error_dictionary["MESSAGE"] = "Error while connecting to device. Check port and connection type."
        else:
            error_dictionary["MESSAGE"] = str(e)
        # SEND ERROR MESSAGE TO CLIENT
        return error_dictionary
    except EOFError as e:
        error_dictionary["STATUS"] = "Failure"
        error_dictionary["TYPE"] = "EOFError"
        error_dictionary["MESSAGE"] = str(e)
        # SEND ERROR MESSAGE TO CLIENT
        return error_dictionary
    except Exception as unknown_error:
        error_dictionary["STATUS"] = "Failure"
        error_dictionary["TYPE"] = "unknown error"
        error_dictionary["MESSAGE"] = str(unknown_error)
        # SEND ERROR MESSAGE TO CLIENT
        return error_dictionary


class ConnectToDevice(object):
    """
    This class pretend to establish a connection to a network device.

    It has 4 functions (static methods):
        - configure_add_raw_commands : send a cisco command to a device. it not run on privileged mode
        - configure_add_raw_commands_not_privileged:  send a cisco command to a device on privileged mode.
        - configures_add_commands_list: send a list of cisco commands to device: it runs on privileged mode.
            (it puts the CLI prompt on: device_name<config>    )
        - save_running_config - save running configurations on cisco network devices

    We could build this code as functions because we don't change anything in the instance object properties of the
    class

    This clas dont validate any data passed to the class. we are assuming that the data is ok.


    :param data: <dict> keys: "ip" - device ip to establish a connection
    :param connection_type <string> WE are expecting "SSH" or "TELNET" as strings for this parameter
                                            ** THIS OPTIONAL PARAMETER

    :param port <int> a port to connect    ** THIS PARAMETER IS OPTIONAL
    :return , check each method, since each one can export different types of data

    ====================================================================================================================

    ## NETMIKO SUPPORTS THIS CISCO DEVICES: (in 2019 Was different)
    ## CISCO DEVICES DRIVERS SUPORTED BY NETMIKO in 2020:
    ## ["cisco_asa", "cisco_ios", "cisco_nxos", "cisco_s300", "cisco_tp", "cisco_wlc", "cisco_xe", "cisco_xr"]


    ## WE suppose, (but not confirmed) that NETMIKO 2020 uses Cisco pyATS and Cisco Gennie 'capabilities' to connect to
    the new Cisco operating systems running on new devices. (e.g. nexos)
    ** We may want to automate configurations on network devices directly through Python pyATS and gennie or Ansible
        source: https://developer.cisco.com/docs/pyats/#!introduction/cisco-pyats-network-test--automation-solution

    # NETMIKO SOURCE LINKS:
        - source: https://ktbyers.github.io/netmiko/docs/netmiko/cisco_base_connection.html
        - source: https://ktbyers.github.io/netmiko/docs/netmiko/index.html
        - source: https://pynet.twb-tech.com/blog/automation/netmiko.html
        - source: https://github.com/ktbyers/netmiko

    ## DEVELOPMENT ENVIRONMENT
    In 2019, we were using 'cisco_ios' driver for ssh connections. and "cisco_ios_telnet" for telnet connections
    It proved to work properly on the devices that we test.
    We have implemented netmiko new feature SSHdiscover that tries to guess which operating system is running on device
    and choose for us the the correspondent device_driver for better interaction.
    We don't know which NETWORK device, CLIENTS WANT TO CONNECT, JUST THE IP.
    NOTE:
    May consider to be mandatory in future requests, that clients send us the OS Device Type instead of just telnet or
    ssh. Or have access to a database table or a file with a mapping between "ip">> "OS type".

    We have tested on these 2 Cisco devices:
        Cisco device 1:
            - Model:  WS-C3560-48PS
            - IOS VERSION: 12.2(53)SE2
        Cisco device 2:
            - Model:  WS-C2950T-24
            - IOS VERSION: 12.1(22)EA14
    --------------------------------------------------------------------------------------------------------------------
        NOTE: if we run problems when connecting to devices(slow networks, slow equipment , etc.) we may consider in
        adjusting and override global_delay_factor for connections.) We can pass as« a key,value pair when we call the
        ConnectHandler method.

        Rationale: netmiko  send_command << will wait 100 seconds by default, which corresponds to default, global_delay_factor=1,
                    if set to:
                        gobal_delay_factor=2  it will duplicate the amount of time
                        goblal_delay_factor=3 will triplicate
                        and so on ...
    --------------------------------------------------------------------------------------------------------------------
    Methods  in MODULE netmiko.cisco_base_connection. THEY ARE USEFUL IF WE NEED TO BUILD MORE functionalities
        - check_config_mode--> Checks if the device is in configuration mode or not.
        - check_enable_mode--> Check if in enable mode. Return boolean.
        - cleanup: Gracefully--> exit the SSH session.
        - config_mode--> Enter into configuration mode on remote device.
        - enable--> Enter enable mode.
        - exit_config_mode--> Exit from configuration mode.
        - exit_enable_mode--> Exits enable (privileged exec) mode.
        - save_config--> Saves Config.
        - serial_login
        - telnet_login

    ###
    ### LAST NOTE:
    Since one of the goals of the development of this application was to present me (the processes of
    writing an app) And i had no knowledge of the oop programming paradigm, I think this class could be better
    constructed using python class inheritance.
        e.g.    class ConnectToDevice(Netmiko):



    """

    # init method
    def __init__(self, data, connection_type, port=None):
        # class attributes

        # TODO: # WE SHOULD CONSIDER TO USE THIS credenctiasl as an(APLICATION  ENV) decrypted
        #  from disk WHENEVER OUR APP STARTS
        self.device_credentials = {"device_username": current_app.config["DEVICE_USERNAME"],
                                   "device_password": current_app.config["DEVICE_PASSWORD"],
                                   "device_secret": current_app.config["DEVICE_SECRET"]
                                   }
        self.data = data
        self.connection_type = connection_type
        self.port = port
        print("=" * 79)
        print("OUTPUT - port: ", port)
        print("OUTPUT - connection_type: ", connection_type)
        print("=" * 79)
        if self.connection_type == "TELNET":
            self.connection_type = "cisco_ios_telnet"
            if port is None:
                self.port = 23

        if self.connection_type == "SSH":
            # FOR SSH  WE WILL TRY TO GUESS FIRST THE BEST MATCH
            if port is None:
                self.port = 22

            # INSERT TEST GUESS HERE
            ssh_device_driver = guess_device(ip=self.data["ip"], port=self.port)
            print("OUTPUT - -----------------------------------------------------------------")
            print("OUTPUT - GUESSING THE SSH DEVICE DRIVER")
            print("OUTPUT - ssh device driver best match is :", ssh_device_driver)
            if isinstance(ssh_device_driver, dict):
                if "STATUS" in ssh_device_driver:
                    if ssh_device_driver["STATUS"] == "Failure":
                        print(" WE COULDNT GUESS THE DEVICE DRIVER FOR SSH")
                        # LETS USE DEFAULT DEVICE DRIVER
                        self.connection_type = "cisco_ios"
            else:
                self.connection_type = ssh_device_driver

        print("OUTPUT - ---------------------")
        print("OUPTUT - INSTANCE OBJECT- ConnectToDevice - __INIT__ METHOD")
        print("OUTPUT - Preparing to connect to device with this setup:")
        print("OUTPUT - device ip: ", self.data["ip"])
        print("OUTPUT - connection_type: ", self.connection_type)
        print("OUTPUT - port: ", self.port)

        # (STANDARD FAILURE DICTIONARY) AND SET VALUES FOR THIS OPERATION ERROR
        self.error_dictionary = {"STATUS": "Failure",
                                 "ERROR": "4",
                                 "TYPE": {},
                                 "MESSAGE": {}
                                 }

    def configure_add_raw_commands(self, command_to_send):
        """
        THIS FUNCTION send  a command to a cisco network device in privileged mode
        :param command_to_send: <string>
        :return: <tupple> a tuple with 2 items. one item is a structured result if netmiko could parse the data
        The second item will be unparsed data, result of the command output in the network device CLI
        """

        print("OUTPUT - Entering...  configure_add_raw_commands --> METHOD           ")
        try:
            # ESTABLISH A  CONNECTION TO DEVICE USING NETMIKO
            self.net_connect = ConnectHandler(device_type=self.connection_type,
                                              ip=self.data["ip"],
                                              username=self.device_credentials["device_username"],
                                              password=self.device_credentials["device_password"],
                                              secret=self.device_credentials["device_secret"],
                                              port=self.port)

            # ENTER PRIVILEGED MODE -- like we put enable in the cisco console.
            self.net_connect.enable()

            # ELIMINATES DE "MORE" WORD ON CISCO TERMINAL - USER DOESN'T HAVE TO PRESS A KEY TO CONTINUE
            self.net_connect.send_command('terminal length 0')

            # WE want to try to get structured data from the cli output but it is only possible
            # TEXTFSM - ntc templates were installed
            try:
                output_structured = self.net_connect.send_command(command_to_send, use_textfsm=True)
            # DESEINTALAR O PATH OU ALTERAR PARA OUTRA LOCALIZACAO NAO EXISTENTE E VER O TIPO DE ERRO QUE DA_
            # Esta excepcao não é a melhor forma de apanhar errors
            except Exception:
                output_structured = None
            output_unstructured = self.net_connect.send_command(command_to_send, use_textfsm=False)
            self.net_connect.send_command('terminal length 24')
            # disconnect from device
            self.net_connect.disconnect()
            return output_structured, output_unstructured

        # CATCH ERRORS AND RETURN THEM
        except AuthenticationException as e:
            self.error_dictionary["STATUS"] = "Failure"
            self.error_dictionary["TYPE"] = "AuthenticationException"
            self.error_dictionary["MESSAGE"] = str(e)
            # SEND ERROR MESSAGE TO CLIENT
            return self.error_dictionary
        except NetMikoTimeoutException as e:
            self.error_dictionary["STATUS"] = "Failure"
            self.error_dictionary["TYPE"] = "NetMikoTimeoutException"
            self.error_dictionary["MESSAGE"] = str(e)
            # SEND ERROR MESSAGE TO CLIENT
            return self.error_dictionary
        except SSHException as e:
            self.error_dictionary["STATUS"] = "Failure"
            self.error_dictionary["TYPE"] = "SSH_exception"
            if "Error reading SSH protocol banner" in str(e):
                self.error_dictionary["MESSAGE"] = "Error while connecting to device. Check port and connection type."
            else:
                self.error_dictionary["MESSAGE"] = str(e)
            # SEND ERROR MESSAGE TO CLIENT
            return self.error_dictionary
        except EOFError as e:
            self.error_dictionary["STATUS"] = "Failure"
            self.error_dictionary["TYPE"] = "EOFError"
            self.error_dictionary["MESSAGE"] = str(e)
            # SEND ERROR MESSAGE TO CLIENT
            return self.error_dictionary
        except Exception as unknown_error:
            self.error_dictionary["STATUS"] = "Failure"
            self.error_dictionary["TYPE"] = "unknown error"
            self.error_dictionary["MESSAGE"] = str(unknown_error)
            # SEND ERROR MESSAGE TO CLIENT
            return self.error_dictionary

    def configure_add_raw_commands_not_privileged(self, command_to_send):
        """
        THIS FUNCTION send  a command to a cisco network device not in privileged mode.
        :param command_to_send: <string>
        :return: <tupple> a tuple with 2 items. one item is a structured result if netmiko could parse the data
        The second item will be unparsed data, result of the command output in the network device CLI
        """

        print("OUTPUT - Entering...  configure_add_raw_commands_not_privileged --> METHOD           ")
        try:
            # ESTABLISH A  CONNECTION TO DEVICE USING NETMIKO
            self.net_connect = ConnectHandler(device_type=self.connection_type,
                                              ip=self.data["ip"],
                                              username=self.device_credentials["device_username"],
                                              password=self.device_credentials["device_password"],
                                              secret=self.device_credentials["device_secret"],
                                              port=self.port)
            # ENTER PRIVILEGED MODE -- like we put enable in the cisco console.
            # self.net_connect.enable()

            # WE CAN RUN COMMANDS not in privileged mode on the cisco cli:
            # EXAMPLE : WE can run --> show version and it will output the result
            # But, if we run a show run :
                    # switchTelnet > show run
                    #                     ^
                    # % Invalid input detected at '^' marker.
            # because we are not in privileged mode

            # ELIMINATES DE "MORE" WORD ON CISCO TERMINAL - USER DOESN'T HAVE TO PRESS A KEY TO CONTINUE
            self.net_connect.send_command('terminal length 0')

            # WE want to try to get structured data from the cli output but it is only possible
            # TEXTFSM - ntc templates were installed
            try:
                output_structured = self.net_connect.send_command(command_to_send, use_textfsm=True)
            # DESEINTALAR O PATH OU ALTERAR PARA OUTRA LOCALIZACAO NAO EXISTENTE E VER O TIPO DE ERRO QUE DA_
            # Esta excepcao não é a melhor forma de apanhar errors
            except Exception:
                output_structured = None
            output_unstructured = self.net_connect.send_command(command_to_send, use_textfsm=False)
            self.net_connect.send_command('terminal length 24')
            # disconnect from device
            self.net_connect.disconnect()
            return output_structured, output_unstructured

        # CATCH ERRORS AND RETURN THEM
        except AuthenticationException as e:
            self.error_dictionary["STATUS"] = "Failure"
            self.error_dictionary["TYPE"] = "AuthenticationException"
            self.error_dictionary["MESSAGE"] = str(e)
            # SEND ERROR MESSAGE TO CLIENT
            return self.error_dictionary
        except NetMikoTimeoutException as e:
            self.error_dictionary["STATUS"] = "Failure"
            self.error_dictionary["TYPE"] = "NetMikoTimeoutException"
            self.error_dictionary["MESSAGE"] = str(e)
            # SEND ERROR MESSAGE TO CLIENT
            return self.error_dictionary
        except SSHException as e:
            self.error_dictionary["STATUS"] = "Failure"
            self.error_dictionary["TYPE"] = "SSH_exception"
            if "Error reading SSH protocol banner" in str(e):
                self.error_dictionary["MESSAGE"] = "Error while connecting to device. Check port and connection type."
            else:
                self.error_dictionary["MESSAGE"] = str(e)
            # SEND ERROR MESSAGE TO CLIENT
            return self.error_dictionary
        except EOFError as e:
            self.error_dictionary["STATUS"] = "Failure"
            self.error_dictionary["TYPE"] = "EOFError"
            self.error_dictionary["MESSAGE"] = str(e)
            # SEND ERROR MESSAGE TO CLIENT
            return self.error_dictionary
        except Exception as unknown_error:
            self.error_dictionary["STATUS"] = "Failure"
            self.error_dictionary["TYPE"] = "unknown error"
            self.error_dictionary["MESSAGE"] = str(unknown_error)
            # SEND ERROR MESSAGE TO CLIENT
            return self.error_dictionary

    def configure_add_commands_list(self, commands_list):

        """
        THIS FUNCTION RECEIVE A LIST WITH CISCO CLI COMMNANDS , AND SEND ThEM TO A NETWORK DEVICE

        :param commands_list: list of command to sento to device NOTE. EACH ITEM SHOUD BE A STRING
        :return: <string> with all the cli device captured by netmiko
        """
        print("OUTPUT - HERE--------------------configure_add_commands_list method----------------")
        try:
            # ESTABLISH A  CONNECTION TO DEVICE USING NETMIKO
            self.net_connect = ConnectHandler(device_type=self.connection_type,
                                              ip=self.data["ip"],
                                              username=self.device_credentials["device_username"],
                                              password=self.device_credentials["device_password"],
                                              secret=self.device_credentials["device_secret"],
                                              port=self.port)

            # enter user exec mode
            self.net_connect.enable()

            # ELIMINATES DE "MORE" WORD ON CISCO TERMINAL - USER DOESN'T HAVE TO PRESS A KEY TO CONTINUE
            self.net_connect.send_command('terminal length 0')

            #output_list= []
            #for command in commands_list:
            #    output = self.net_connect.send_command(command, use_textfsm=True)
            #    output_list.append(output)

            # WE COULD SEND ALL THE COMMANDS ONE ONE TIME.
            output = self.net_connect.send_config_set(commands_list)

            # SET CONSOLE TO DEFAULTS 24 LINES - IT WILL SHOW AGAIN "MORE" WHEN USER RUN COMMANDS LIKE "SHOW VLAN"
            self.net_connect.send_command('terminal length 24')
            # DISCONNECT FROM DEVICE
            self.net_connect.disconnect()
            return output

        # CATCH ERRORS AND RETURN THEM
        except AuthenticationException as e:
            self.error_dictionary["STATUS"] = "Failure"
            self.error_dictionary["TYPE"] = "AuthenticationException"
            self.error_dictionary["MESSAGE"] = str(e)
            # SEND ERROR MESSAGE TO CLIENT
            return self.error_dictionary
        except NetMikoTimeoutException as e:
            self.error_dictionary["STATUS"] = "Failure"
            self.error_dictionary["TYPE"] = "NetMikoTimeoutException"
            self.error_dictionary["MESSAGE"] = str(e)
            # SEND ERROR MESSAGE TO CLIENT
            return self.error_dictionary
        except SSHException as e:
            self.error_dictionary["STATUS"] = "Failure"
            self.error_dictionary["TYPE"] = "SSH_exception"
            if "Error reading SSH protocol banner" in str(e):
                self.error_dictionary["MESSAGE"] = "Error while connecting to device. Check port and connection type."
            else:
                self.error_dictionary["MESSAGE"] = str(e)
            # SEND ERROR MESSAGE TO CLIENT
            return self.error_dictionary
        except EOFError as e:
            self.error_dictionary["STATUS"] = "Failure"
            self.error_dictionary["TYPE"] = "EOFError"
            self.error_dictionary["MESSAGE"] = str(e)
            # SEND ERROR MESSAGE TO CLIENT
            return self.error_dictionary
        except Exception as unknown_error:
            self.error_dictionary["STATUS"] = "Failure"
            self.error_dictionary["TYPE"] = "unknown error"
            self.error_dictionary["MESSAGE"] = str(unknown_error)
            # SEND ERROR MESSAGE TO CLIENT
            return self.error_dictionary

    def save_running_config(self):

        """
        THIS FUNCTION save the running configurations in the start up configuration file
        :return: <string> with all the cli device captured by netmiko

        rationale:
        They essentially achieve the same things by saving the running configuration to the memory so that after a
        reload it retains the same configuration. Write memory is the "ancient" way, and
        copy running-config startup-config is the "newer way".
        Some newer platforms do not accept write memory, the Nexus platforms for instance.

        The workaround is to create an alias using cli alias name wr copy run start in global configuration mode.

        The "copy run start" command is just a variation of the "copy" command. The copy command can be used to copy any
        files in or out of the flash etc. - as opposed to just saving the configuration. Just remember though, if you
        are in the wrong configuration register "wr" will lose your configuration after a reload/when you change
        the configuration register whereas "copy run start" will just copy the contents of the running
        configuration to the start-up configuration.
        When doing CCNA exams, the command "write" is not allowed.
        It has to be the official "copy running-config startup-config".
        The reason why the "wr" or "write" command is very popular are:
            - A minimum of two characters to save a config;
            - It is easy to confuse "copy start run" with "copy run start".

        # SOURCE: https://ktbyers.github.io/netmiko/docs/netmiko/cisco_base_connection.html#netmiko.cisco_base_connection.CiscoBaseConnection.save_config

        """
        print("OUTPUT - HERE--------------------save_running_config method----------------")
        try:
            # ESTABLISH A  CONNECTION TO DEVICE USING NETMIKO
            self.net_connect = ConnectHandler(device_type=self.connection_type,
                                              ip=self.data["ip"],
                                              username=self.device_credentials["device_username"],
                                              password=self.device_credentials["device_password"],
                                              secret=self.device_credentials["device_secret"],
                                              port=self.port)

            #SOURCE: https://github.com/ktbyers/netmiko/blob/develop/examples/enable/enable.py
            # Enter enable mode
            self.net_connect.enable()
            #print(self.net_connect.find_prompt())

            # SEND SAVE COMMAND TO DEVICE
            output = self.net_connect.save_config(cmd="copy running-config startup-config",
                                                  confirm=True,
                                                  confirm_response="")

            # DISCONNECT FROM DEVICE
            self.net_connect.disconnect()
            # RETURN THE OUTPUT OF THE CONSOLE OUT
            return output

        # CATCH ERRORS AND RETURN THEM
        except AuthenticationException as e:
            self.error_dictionary["STATUS"] = "Failure"
            self.error_dictionary["TYPE"] = "AuthenticationException"
            self.error_dictionary["MESSAGE"] = str(e)
            # SEND ERROR MESSAGE TO CLIENT
            return self.error_dictionary
        except NetMikoTimeoutException as e:
            self.error_dictionary["STATUS"] = "Failure"
            self.error_dictionary["TYPE"] = "NetMikoTimeoutException"
            self.error_dictionary["MESSAGE"] = str(e)
            # SEND ERROR MESSAGE TO CLIENT
            return self.error_dictionary
        except SSHException as e:
            self.error_dictionary["STATUS"] = "Failure"
            self.error_dictionary["TYPE"] = "SSH_exception"
            if "Error reading SSH protocol banner" in str(e):
                self.error_dictionary["MESSAGE"] = "Error while connecting to device. Check port and connection type."
            else:
                self.error_dictionary["MESSAGE"] = str(e)
            # SEND ERROR MESSAGE TO CLIENT
            return self.error_dictionary
        except EOFError as e:
            self.error_dictionary["STATUS"] = "Failure"
            self.error_dictionary["TYPE"] = "EOFError"
            self.error_dictionary["MESSAGE"] = str(e)
            # SEND ERROR MESSAGE TO CLIENT
            return self.error_dictionary
        except Exception as unknown_error:
            self.error_dictionary["STATUS"] = "Failure"
            self.error_dictionary["TYPE"] = "unknown error"
            self.error_dictionary["MESSAGE"] = str(unknown_error)
            # SEND ERROR MESSAGE TO CLIENT
            return self.error_dictionary



