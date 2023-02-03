import yfinance as yf
from datetime import datetime
from modules.fileManager.fileManager import FileManager
from modules.scraper.yahooFinanceScrapper import YahooFinanceScraper
from modules.scraper import constants

class BackEnd(FileManager):
    """
    Class to handle Back End
    """
    def __init__(self, dataFolder : str):
        super().__init__()
        self.setRootFolder(dataFolder)
        self.__previousYear = str(datetime.now().year - 1)

        self.scraper = YahooFinanceScraper()

    def saveStock(self, row):
        """
        Method to save a stock row in a csv file
        """
        if FileManager.checkFileExists(self.getPaths()["finance"]["stocks"]["stocksCsv"]):
            with open(self.getPaths()["finance"]["stocks"]["stocksCsv"], "a") as stockCsvFile:
                stockCsvFile.write(row + "\n")
        else:
            with open(self.getPaths()["finance"]["stocks"]["stocksCsv"], "w") as stockCsvFile:
                stockCsvFile.write("country,stock,name,dividendYiel,currentPrice,currency,enterpriseValue\n")
                stockCsvFile.write(row + "\n")

    def downloadAllStocks(self):
        """
        Method to get all the stocks
        """
        stocksJson = self.getPaths()["finance"]["stocks"]["stocksJson"]

        stocks = self.scraper.scrapeAllStocks()

        FileManager.saveJson(stocksJson, stocks)

        return stocks

    def downloadStocksCountry(self, country : str):
        """
        Method to get all stocks using a path
        """
        stocksJson = self.getPaths()["finance"]["stocks"]["stocksJson"]

        stocks = self.scraper.scrapeStocksCountry(country)

        FileManager.saveJson(stocksJson, stocks)

        return stocks

    def getDividends(self, stock : str):
        """
        Method to obtain dividend
        """
        return float(sum(yf.Ticker(stock).actions.loc["2022"].Dividends))

    def getStock(self, stock):
        """
        Method to get stock info
        """
        stockData = self.scraper.getStockData(stock)
        return stockData["enterpriseValue"], stockData["averagePrice"], stockData["dividendYield"], stockData["currency"]

    def getAllStocksInfo(self):
        """
        Method to get info of all the stocks
        """
        stocksJson = self.getPaths()["finance"]["stocks"]["stocksJson"]

        stocks = FileManager.loadJson(stocksJson)

        for country in stocks.keys():
            for stock in stocks[country].keys():
                try:
                    enterpriseValue, averagePrice, dividendYield, currency = self.getStock(stock)
                    if dividendYield == 0.0 or dividendYield == "N/A":
                        pass
                    elif dividendYield == "":
                        print(enterpriseValue)
                        print(averagePrice)
                        print(dividendYield)
                        print(currency)
                        return
                    else:
                        stockRow = constants.countries[country] + "," + stock + "," + stocks[country][stock].replace(",", "") + "," + str(dividendYield) + "," + str(averagePrice) + "," +  str(currency) + "," + str(enterpriseValue)
                        self.saveStock(stockRow)
                except Exception as e:
                    print("Error in stock: " + stock)
                    print(e)
