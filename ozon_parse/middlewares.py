from scrapy.http import HtmlResponse
from selenium.webdriver import ActionChains, Chrome, ChromeOptions


class SeleniumMiddleWare:
    def __init__(self):
        options = ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.default_content_setting_values.notifications": 2,
            "profile.managed_default_content_settings.stylesheets": 2,
            "profile.managed_default_content_settings.javascript": 1,
            "profile.managed_default_content_settings.plugins": 1,
            "profile.managed_default_content_settings.popups": 2,
            "profile.managed_default_content_settings.geolocation": 2,
            "profile.managed_default_content_settings.media_stream": 2,
        }
        options.add_experimental_option("prefs", prefs)

        driver_path = "../chromedriver"
        self.driver = Chrome(executable_path=driver_path, options=options)
        self.driver.get("https://www.ozon.ru/category/smartfony-15502/?sorting=rating")
        ActionChains(self.driver).scroll_by_amount(0, 1000).pause(10).perform()
        self.driver.delete_all_cookies()

    def process_request(self, request, spider):
        self.driver.get(request.url)
        ActionChains(self.driver).scroll_by_amount(0, 1000).pause(5).perform()
        content = self.driver.page_source
        self.driver.delete_all_cookies()
        return HtmlResponse(
            request.url, encoding="utf-8", body=content, request=request
        )

    def process_response(self, request, response, spider):
        return response

