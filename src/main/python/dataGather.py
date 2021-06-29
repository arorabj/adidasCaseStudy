from src.main.python.loggerInitialisation import *
from src.main.python.readConfig import *
import pandas as pd
import json

env="dev"
fileName="ol_cdump.json"
confPath = '../../../resources/config/application.properties'


pd.set_option('display.max_rows', None)

def read_file(fileName: str, env: str, confPath: str):
    """
    Description :
    This function read the property file to get the details of input directory
    :param fileName: File name of file to be read
    :param env: Env in which script is running
    :param confPath: Path of Config File

    Output:
    :return:
    """
    try :
        fileDirectory = read_config(confPath,env,"inputDirectory")
        filePath = fileDirectory+"/"+fileName

        if os.path.isfile(filePath) :
            logger.info(f"Data file is present at {filePath}. Going to read the datafile ")

            chunkSize = read_config(confPath, env, "chunkSize")
            if chunkSize is None:
                chunkSize = "1000"
            else:
                chunkSize = int(chunkSize)

            df= pd.read_json(filePath,lines=True)

            # create copy of exiting df

            dfCleanTitle= df.copy()

            # clean title
            dfCleanTitle= dfCleanTitle[dfCleanTitle['title'].notnull()]
            dfCleanTitle= dfCleanTitle[dfCleanTitle['title']!= 'No Title Exists.']

            # clean NumberOfPages
            dfCleanNumberOfPages = dfCleanTitle.copy()
            dfCleanNumberOfPages = dfCleanNumberOfPages[dfCleanNumberOfPages['number_of_pages'].fillna(0).notnull().astype(str)]
            #dfCleanNumberOfPages = dfCleanNumberOfPages[dfCleanNumberOfPages['dfCleanNumberOfPages'] >= 'No Title Exists.']
            print(dfCleanNumberOfPages['number_of_pages'].value_counts())
            #dfCleanPublishingYear = dfCleanTitle[dfCleanTitle['title'] != 'No Title Exists.']

            #print(dfCleanTitle['title'].value_counts())

            # df_clean_title= df.filter()
        else:
            logger.error(f"Data file is not present")
            raise SystemExit("Program Finished with Error")
    except Exception as e:
        logger.error(f"Error :{e}")


read_file(fileName,env,confPath)