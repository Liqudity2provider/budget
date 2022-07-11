import time
# sudo apt-get install chromium-chromedriver
import uuid

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from budget_django.settings import STATIC_URL


class MonoIntegrationUtil:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--incognito")

        self.browser = webdriver.Chrome(chrome_options=chrome_options)

        self.browser.get("https://api.monobank.ua/")

    def get_qr_path(self):
        time.sleep(2)
        qr_path = str(uuid.uuid4())
        qr = self.browser.find_element(
            by='xpath',
            value='//*[@id="qrcode"]/img').screenshot(
            f"{STATIC_URL}{qr_path}.png")

        return qr_path + ".png"

    def get_token(self):
        time.sleep(2)
        for i in range(600):
            try:
                qr_code = self.browser.find_element(
                    by='xpath',
                    value='//*[@id="qrcode"]/img')
                if not qr_code.size.get("height") and not qr_code.size.get(
                        "width"):
                    break
            except NoSuchElementException:
                pass
            time.sleep(0.5)

        try:
            activate_button = self.browser.find_element(
                "xpath",
                '//*[@id="user"]/div/button')
            activate_button.click()
        except NoSuchElementException:
            pass

        time.sleep(1)
        mono_token = None

        try:
            token_from_page = self.browser.find_element(
                by="xpath",
                value='//*[@id="user"]/div/span[2]')
        except NoSuchElementException:
            print("error with token search")

        else:
            mono_token = token_from_page.text
            print("Success!")
        finally:
            self.browser.close()
            return mono_token
