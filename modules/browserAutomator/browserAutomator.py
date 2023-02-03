import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webelement import RemoteWebElement
from webdriver_manager.firefox import GeckoDriverManager
from modules.browserAutomator import constants

class BrowserAutomator(object):
    """
    Class to automate browser interactions
    """
    def __init__(self):
        self.__url = None
        self.__delay = constants.delayBrowserAutomation

        options = webdriver.FirefoxOptions()
        options.add_argument("-headless")
        self.browser = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)

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

    def startSession(self, path : str):
        """
        Method to start a session for browser automation
        """
        assert self.__url is not None, "main url has not been set"

        self.browser.get(self.__url + path)

    def getButtonByText(self, text : str):
        """
        Get button
        """
        return self.browser.find_element(By.XPATH, '//button[normalize-space()="' + text + '"]')

    def clickButtonByText(self, buttonName : str, retry=False):
        """
        Method to click in a button
        """
        assert self.__url is not None, "main url has not been set"
        time.sleep(constants.delayBrowserAutomation)
        retries = 0
        error = ""
        if retry:
            while(retries < constants.retries):
                try:
                    button = self.browser.find_element(By.XPATH, '//button[normalize-space()="' + buttonName + '"]')
                    break
                except Exception as e:
                    time.sleep(constants.delayBrowserAutomation)
                    error = e
                retries += 1
            if retries == constants.retries:
                raise Exception("Max retries reached: " + str(constants.retries) + ", with error: " + str(error))
        else:
            button = self.browser.find_element(By.XPATH, '//button[normalize-space()="' + buttonName + '"]')
        button.click()

    def clickButtonBy(self, type : str,  text : str, retry=False):
        """
        Method to click in a button by value
        """
        assert self.__url is not None, "main url has not been set"
        time.sleep(constants.delayBrowserAutomation)
        retries = 0
        error = ""
        if retry:
            while(retries < constants.retries):
                try:
                    button = self.browser.find_element(By.XPATH, '//button[@' + type + '="' + text + '"]')
                    break
                except Exception as e:
                    time.sleep(constants.delayBrowserAutomation)
                    error = e
                retries += 1
            if retries == constants.retries:
                raise Exception("Max retries reached: " + str(constants.retries) + ", with error: " + str(error))
        else:
            button = self.browser.find_element(By.XPATH, '//button[@' + type + '="' + text + '"]')
        button.click()

    def clickSpanByText(self, text : str, retry=False):
        """
        Method to click in a span by text
        """
        assert self.__url is not None, "main url has not been set"
        time.sleep(constants.delayBrowserAutomation)
        retries = 0
        error = ""
        if retry:
            while(retries < constants.retries):
                try:
                    button = self.browser.find_element(By.XPATH, '//span[text()="' + text + '"]')
                    break
                except Exception as e:
                    time.sleep(constants.delayBrowserAutomation)
                    error = e
                retries += 1
            if retries == constants.retries:
                raise Exception("Max retries reached: " + str(constants.retries) + ", with error: " + str(error))
        else:
            button = self.browser.find_element(By.XPATH, '//span[text()="' + text + '"]')
        button.click()

    def getElementByType(self, type : str, retry=False):
        """
        Method to get element by type
        """
        assert self.__url is not None, "main url has not been set"
        time.sleep(constants.delayBrowserAutomation)
        retries = 0
        error = ""
        if retry:
            while(retries < constants.retries):
                try:
                    element = self.browser.find_element(By.XPATH, '//' + type)
                    break
                except Exception as e:
                    time.sleep(constants.delayBrowserAutomation)
                    error = e
                retries += 1
            if retries == constants.retries:
                raise Exception("Max retries reached: " + str(constants.retries) + ", with error: " + str(error))
        else:
            element = self.browser.find_element(By.XPATH, '//' + type)

        return element

    def getElementByText(self, text : str, retry=False):
        """
        Method to get element by text
        """
        assert self.__url is not None, "main url has not been set"
        time.sleep(constants.delayBrowserAutomation)
        retries = 0
        error = ""
        if retry:
            while(retries < constants.retries):
                try:
                    element = self.browser.find_element(By.XPATH, '//*[text()="' + text + '"]')
                    break
                except Exception as e:
                    time.sleep(constants.delayBrowserAutomation)
                    error = e
                retries += 1
            if retries == constants.retries:
                raise Exception("Max retries reached: " + str(constants.retries) + ", with error: " + str(error))
        else:
            element = self.browser.find_element(By.XPATH, '//*[text()="' + text + '"]')

        return element

    def getParentFromElement(self, element : RemoteWebElement, level : int):
        """
        Return parent of an element
        """
        for iteration in range(level):
            element = element.find_element(By.XPATH, "..")

        return element

    def getChildByIndex(self, element : RemoteWebElement, index : int):
        """
        Method to return child element by index
        """
        return element.find_elements(By.XPATH, "./*")[index]

    def getTextByContainedText(self, text : str):
        """
        Method to return text using a contained text
        """
        element = self.browser.find_element(By.XPATH, "//*[contains(text(), '" + text + "')]")
        return element.text

    def finishSession(self):
        """
        Method to finish a session
        """
        self.browser.close()
