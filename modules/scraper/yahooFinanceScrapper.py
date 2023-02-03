import requests
from modules.fileManager.fileManager import FileManager
from modules.scraper.scraper import Scraper
from modules.browserAutomator.browserAutomator import BrowserAutomator
from modules.scraper import constants

class YahooFinanceScraper(Scraper):
    """
    Class to scrape yahoo finance
    """
    def __init__(self):
        super().__init__()
        self.setUrl(constants.yahooFinanceUrl)

        self.browserAutomator = BrowserAutomator()
        self.browserAutomator.setUrl(constants.yahooFinanceUrl)

    def scrapeStocks(self, country):
        """
        Method to scrape stocks from browser
        """
        finished = False
        if FileManager.checkFileExists(constants.stocksJson):
            stocks = FileManager.loadJson(constants.stocksJson)
        else:
            stocks = {}

        while finished is False:
            table = self.browserAutomator.getElementByType("table", retry=True).text
            rows = table.split("\n")
            # 2 starting row because header
            for i in range(2, len(rows), 2):
                elementsStock = rows[i + 1].split(" ")
                numberElementsName = len(elementsStock) - 7
                if country in stocks:
                    stocks[country].update({
                        rows[i] : " ".join(elementsStock[0 : numberElementsName])
                    })
                else:
                    stocks.update({
                        country : {
                            rows[i] : " ".join(elementsStock[0 : numberElementsName])
                        }
                    })

            FileManager.saveJson(stocks, constants.stocksJson)

            button = self.browserAutomator.getButtonByText("Next")

            if button.get_attribute("aria-disabled") == "true":
                finished = True
            else:
                button.click()

    def scrapeStocksCountry(self, country : str):
        """
        Method to scrape all stocks using path
        """
        try:
            self.browserAutomator.startSession("/screener/equity/new/")
            try:
                self.browserAutomator.clickButtonBy("value", "agree")
            except:
                pass
            self.browserAutomator.clickButtonBy("title", "Remove United States")
            self.browserAutomator.clickSpanByText("Add ")
            self.browserAutomator.clickSpanByText(
                constants.countries[country]
            )
            self.browserAutomator.clickButtonBy("title", "Close")
            self.browserAutomator.clickButtonBy("data-test", "find-stock")
            self.scrapeStocks(country)
        except Exception as e:
            print("Failed in country: " + country)
            self.browserAutomator.finishSession()
            self.browserAutomator.startSession("/screener/equity/new/")

        return FileManager.loadJson(constants.stocksJson)

    def scrapeAllStocks(self):
        """
        Method to scrape all stocks
        """
        for country in list(constants.countries.keys()):
            self.scrapeStocksCountry(country)

        return FileManager.loadJson(constants.stocksJson)

    def getFieldByNameInStockInfo(self, fieldName : str):
        """
        Method to obtain value of a field by name
        """
        elementStock = self.browserAutomator.getElementByText(fieldName)
        parentElementStock = self.browserAutomator.getParentFromElement(elementStock, 2)
        targetElement = self.browserAutomator.getChildByIndex(parentElementStock, 1)

        return targetElement.text

    def getTextByContainedText(self, text : str):
        """
        Method to get a text by regex rule
        """
        return self.browserAutomator.getTextByContainedText(text)

    def getStockData(self, stock):
        """
        Method to scrape specific stock
        """
        stockData = {}
        try:
            self.browserAutomator.startSession("/quote/" + stock + "/key-statistics")
            try:
                self.browserAutomator.clickButtonBy("value", "agree")
                self.browserAutomator.clickButtonBy("aria-label", "Close", retry=True)
            except:
                pass
            enterpriseValue = self.getFieldByNameInStockInfo("Enterprise Value").replace(",", "")
            averagePrice = self.getFieldByNameInStockInfo("200-Day Moving Average").replace(",", "")
            dividendYield = self.getFieldByNameInStockInfo("Forward Annual Dividend Yield")
            currency = self.getTextByContainedText("Currency in ").split("Currency in ")[1]
            stockData.update({
                "enterpriseValue" : enterpriseValue,
                "averagePrice" : averagePrice,
                "dividendYield" : dividendYield,
                "currency" : currency,
            })

        except Exception as e:
            print("Failed stock: " + stock)

        return stockData
