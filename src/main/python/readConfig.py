import configparser as cp
from src.main.python.loggerInitialisation import *

import os


conf = cp.RawConfigParser()

def read_config(confPath: str, env:  str, propKey: str):
    """
    Description :
    This function read the property file to get the details of input directory
    :param conf: Path of Config File
    :param env: env in which script is running
    :param propKey: value of property
    Output:
    :return: property value
    """
    try :
        if os.path.isfile(confPath) :
            logger.info(f"Property file is present at {confPath} ")
            conf.read(confPath)

            propVal = conf.get(env, propKey)
            return propVal

        else:
            logger.error(f"Property file not present")
            raise SystemExit("Program Finished with Error")
    except Exception as e:
        logger.error(f"Error :{e}")

