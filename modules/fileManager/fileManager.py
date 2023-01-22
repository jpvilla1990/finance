import os
import json

class FileManager(object):
    """
    Class to handle files
    """
    def __init__(self):
        self.__initObjects()

    def __initObjects(self):
        self.__rootFolder = None
        self.__paths = None

    def __setPaths(self, root : str):
        financeFolder = "finance"
        stocksFolder = "stocks"
        dictPaths = {
            "path" : root,
            "finance" : {
                "path" : os.path.join(root, financeFolder),
                "stocks" : {
                    "path" : os.path.join(root, financeFolder, stocksFolder),
                }
            }
        }
        return dictPaths

    def checkFileExists(fileName):
        """
        Method to check if file exists
        """
        return os.path.exists(fileName)

    def saveJson(dict, fileName):
        """
        Static method to save json
        """
        with open(fileName, 'w') as jsonFile:
            jsonFile.write(json.dumps(dict, indent=4, sort_keys=True))

    def loadJson(fileName):
        """
        Static method to load json
        """
        with open(fileName, 'r') as jsonFile:
            return json.load(jsonFile)

    def getPaths(self):
        """
        Method to get paths
        """
        return self.__paths

    def setRootFolder(self, folder : str):
        """
        Method to set root folder
        """
        self.__rootFolder = folder
        self.__paths = self.__setPaths(self.__rootFolder)
