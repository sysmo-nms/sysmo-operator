import os
import sys
import logging
import logging.handlers
from PyQt5.QtCore import QStandardPaths



class SysmoLogger:
    def __init__(self, logger, level):
        self.logger = logger
        self.level = level

    def write(self, message):
        if message != '\n':
            self.logger.log(self.level, message)

    def flush(self): pass

def init_logger():
    # get user application data dir
    data = QStandardPaths.writableLocation(QStandardPaths.AppLocalDataLocation)
    # generate sysmo operator dir
    data_sysmo = os.path.join(data, "Sysmo-Operator")
    # create if inexistant
    if os.path.isdir(data_sysmo) == False: os.mkdir(data_sysmo)
    # generate logfile
    LOGFILE = os.path.join(data_sysmo, "operator.log")


    # init logger
    logger = logging.getLogger("sysmo")
    logger.setLevel(logging.DEBUG)
    # create rotating file handler
    rotate = logging.handlers.RotatingFileHandler(LOGFILE, maxBytes=10000, backupCount=5)
    rotate.setLevel(logging.DEBUG)
    # create formater
    formater = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # set it up
    rotate.setFormatter(formater)
    logger.addHandler(rotate)

    # replace sys.stdin and sys.stdout to logging
    mystdout = SysmoLogger(logger, logging.INFO)
    mystderr = SysmoLogger(logger, logging.ERROR)
    sys.stdout = mystdout
    sys.stderr = mystderr
