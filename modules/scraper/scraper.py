import requests
from bs4 import BeautifulSoup

class Scraper(object):
    """
    Class to scrape websites
    """
    def __init__(self):
        self.__url = None

    def setUrl(self, url : str):
        """
        Method to set main url to scrape
        """
        self.__url = url

    def getUrl(self):
        """
        Method to get main url
        """
        return self.__url

    def scrape(self, path : str):
        """
        Method to scrape a path

        return soup
        """
        assert self.__url is not None, "main url has not been set"

        r = requests.get(self.__url + path)
        soup = BeautifulSoup(r.text, "html.parser")

        return soup
