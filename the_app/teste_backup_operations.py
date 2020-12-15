import logging
from logging.handlers import RotatingFileHandler
from os import path, mkdir


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
    logger = logging.getLogger(name)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')

    #logging.getLogger('netmiko')

    logger.name = name
    logger.setLevel(level)
    # add a rotating handler
    handler = RotatingFileHandler(filename=log_file_name,
                                  maxBytes=max_size,
                                  backupCount=number_of_backup_files_to_store)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
