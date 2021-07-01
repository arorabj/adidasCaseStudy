from src.main.python.loggerInitialisation import *
from src.main.python.readConfig import *
import pandas as pd
import json

env="dev"
fileName="ol_cdump.json"
confPath = '../../../resources/config/application.properties'

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 1000)

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
        fileOutDirectory = read_config(confPath, env, "outputDirectory")
        filePath = fileDirectory+"/"+fileName
        filterListPublishingYear=["1969/01","November 15,008","02/02/09","DSD, 1998 Port-au-Prince, Haiti","Estados Unidos","December 2008 / January 2009","2002-2003","Montevideo","Montevideo Uruguay","Nicaragua","Nicaragua,","no","not","suma de letras-Santillana","Talleres Nacionales","u   ","uuuu","vers  1942","Vol.2 1973, Vol. 1 1982, Vol. 3 2009","Madrid","Lima, Perú","hjkhkjh","Guatemala","Erstauflage 1896, Neuauflage 2009","En preparacion","Editorial LA sALLE","Editorial Fray Jodoco Rikie","Editorial Artes Gráficas","editores Testimonio","Editores Testimonio","Editores","ediciones ABYA_YALA","During the british/sikh","Del taller","Caracas, Venezuela","Buenos Aires","BUENOS AIRES","Bogotá, D. C.","Bogotá, Colombia","Bigitá, Colombia","Belgrado, Yugoslavia","Available","Asunción","Artes Gráficas","717u","677u","1uuu","19uu","199u","198u","197u","196u","1960's ?","195u","194u","193u","192u","191u","190u","1900's ?","19--","1900's","18uu","189u","188u","187u","1871 - 1873","185u","184u","183U","1830  Hartford","175u","16uu","12-20-08","9999","2972","3606","3707","5702","5703", "5704","6908","8727","9291","9971","0","180","197","199","918","993","First Edition 2005, Second Edition 2008","first time in 1978, 1990"]

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

            #dfCleanTitle['title'].value_counts().reset_index().to_csv('dfCleanTitle.csv')

            # clean PublishingYear
            dfCleanPublishingYear = dfCleanTitle.copy()
            dfCleanPublishingYear = dfCleanPublishingYear[dfCleanPublishingYear['publish_date'].fillna(0).notnull()]
            dfCleanPublishingYear = dfCleanPublishingYear[~dfCleanPublishingYear['publish_date'].isin(filterListPublishingYear)]
            dfCleanPublishingYear['publish_date'] = dfCleanPublishingYear['publish_date'].str.strip()
            dfCleanPublishingYear['publish_date'] = dfCleanPublishingYear['publish_date'].str[-4:]
            dfCleanPublishingYear = dfCleanPublishingYear[dfCleanPublishingYear['publish_date'].str.len() > 0]
            dfCleanPublishingYear['publish_date'] = dfCleanPublishingYear['publish_date'].astype(int)
            dfCleanPublishingYear = dfCleanPublishingYear[dfCleanPublishingYear['publish_date'] > 1950]

            #dfCleanPublishingYear['publish_date'].value_counts().reset_index().to_csv('PublishingYear.csv')

            # clean NumberOfPages
            dfCleanNumberOfPages = dfCleanPublishingYear.copy()
            dfCleanNumberOfPages['number_of_pages'] = dfCleanNumberOfPages['number_of_pages'].astype(str).str.strip()
            dfCleanNumberOfPages = dfCleanNumberOfPages[dfCleanNumberOfPages['number_of_pages'].str.len() > 0 ]
            dfCleanNumberOfPages = dfCleanNumberOfPages[dfCleanNumberOfPages['number_of_pages']  != "nan"]
            dfCleanNumberOfPages['number_of_pages'] = dfCleanNumberOfPages['number_of_pages'].apply(float)
            dfCleanNumberOfPages['number_of_pages'] = dfCleanNumberOfPages['number_of_pages'].apply(int)
            dfCleanNumberOfPages = dfCleanNumberOfPages[dfCleanNumberOfPages['number_of_pages'] > 20]

            #dfCleanNumberOfPages['number_of_pages'].value_counts().reset_index().to_csv('dfCleanNumberOfPages.csv')

            # Harry potter books
            dfHarryPotter = dfCleanNumberOfPages.copy()
            dfHarryPotter = dfHarryPotter[dfHarryPotter['title'].str.contains("harry", case=False)]
            dfHarryPotter = dfHarryPotter[dfHarryPotter['title'].str.contains("potter", case=False)]
            dfHarryPotter.to_csv(fileOutDirectory + "/" + "HarryPotter.csv")

            # books with max pages
            dfMostPages = dfCleanNumberOfPages.copy()
            dfMostPages = dfMostPages[dfMostPages['number_of_pages'] == dfMostPages['number_of_pages'].max()]
            dfMostPages.to_csv(fileOutDirectory + "/" + "MostPages.csv")

            # Top 5 authors with most written books (assuming author in first position in the array, "key" field and each
            # row is a different book)

            # Find the Top 5 genres with most books

            # Get the avg. number of pages

            # per publish year, get the number of authors that published at least one book



        else:
            logger.error(f"Data file is not present")
            raise SystemExit("Program Finished with Error")
    except Exception as e:
        logger.error(f"Error :{e}")


read_file(fileName,env,confPath)