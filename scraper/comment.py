from time import sleep
from selenium.common.exceptions import (
    NoSuchElementException,
)
from selenium.webdriver.chrome.webdriver import WebDriver

class Comment:
    def __init__(self,
        card: WebDriver,
        ) -> None:
        self.card = card
        self.error = False
        self.comment = None

        try:
            self.user = card.find_element(
                "xpath", './/div[@data-testid="User-Name"]//span'
            ).text
        except NoSuchElementException:
            self.error = True
            self.user = "skip"
        
        try:
            self.handle = card.find_element(
                "xpath", './/span[contains(text(), "@")]'
            ).text
        except NoSuchElementException:
            self.error = True
            self.handle = "skip"

        try:
            self.date_time = card.find_element("xpath", ".//time").get_attribute(
                "datetime"
            )

            if self.date_time is not None:
                self.is_ad = False
        except NoSuchElementException:
            self.is_ad = True
            self.error = True
            self.date_time = "skip"

        if self.error:
            return
        
        self.content = ""
        contents = card.find_elements(
            "xpath",
            '(.//div[@data-testid="tweetText"])[1]/span | (.//div[@data-testid="tweetText"])[1]/a',
        )

        for index, content in enumerate(contents):
            self.content += content.text

        try:
            self.comment_link = self.card.find_element(
                "xpath",
                ".//a[contains(@href, '/status/')]",
            ).get_attribute("href")
            self.comment_id = str(self.comment_link.split("/")[-1])
        except NoSuchElementException:
            self.comment_link = ""
            self.comment_id = ""

        self.comment = (
            self.user,
            self.handle,
            self.date_time,
            self.content,
            self.comment_link,
            self.comment_id,
        )