from modules.fileManager.fileManager import FileManager
from modules.scraper.yahooFinanceScrapper import YahooFinanceScraper

class BackEnd(FileManager):
    """
    Class to handle Back End
    """
    def __init__(self, dataFolder : str):
        super().__init__()
        self.setRootFolder(dataFolder)

        self.scraper = YahooFinanceScraper()

    def downloadAllStocks(self):
        """
        Method to get all the stocks
        """
        stocksPath = self.getPaths()["finance"]["stocks"]["path"]

        print(self.scraper.scrapeAllStocks())

        return {"result": "data"}

    def downloadStocksCountry(self, country : str):
        """
        Method to get all stocks using a path
        """
        stocksPath = self.getPaths()["finance"]["stocks"]["path"]

        print(self.scraper.scrapeStocksCountry(country))

        return {"result": "data"}