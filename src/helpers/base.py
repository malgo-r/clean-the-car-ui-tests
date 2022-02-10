""" Module includes basic commands used in others helpers """

import logging
import os.path
import random
import string
import time
from typing import Union, TypeVar

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    ScreenshotException,
    NoSuchElementException,
    ElementClickInterceptedException,
    ElementNotVisibleException,
    ElementNotSelectableException,
    TimeoutException,
    ElementNotInteractableException,
)

WebElement = TypeVar("WebElement")


class SeleniumDriver:
    """Class includes basic methods to interacting with page elements"""

    def __init__(self, driver):
        self.driver = driver

    locator = None
    locator_type = None
    locator_info = "element with locator %s and locator type: %s", locator, locator_type

    @staticmethod
    def generate_random_string(size: int = 6) -> str:
        """Sample method docstring - todo"""

        return "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(size)
        )

    def take_screen_shot(self, message: str) -> bool:
        """Sample method docstring - todo"""

        file_name = f"{message.replace(' ', '_')}_{round(time.time() * 1000)}.png"
        screen_shot_dir = ".../screenshots/"
        current_dir = os.path.dirname(__file__)
        relative_path_name = screen_shot_dir + file_name
        destination_file = os.path.join(current_dir, relative_path_name)
        destination_directory = os.path.join(current_dir, screen_shot_dir)

        try:
            if not os.path.exists(destination_directory):
                os.makedirs(destination_file)
            if self.driver.instance.sace_screenshot(destination_file):
                logging.info("Screenshot saved to directory: %s", destination_file)
                return True
            return False
        except OSError:
            logging.error("System related error occurred")
            return False
        except ScreenshotException:
            logging.error("Screen not captured")
            return False

    def get_by_type(self, locator_type: str) -> Union[None, bool]:
        """Sample method docstring - todo"""

        locator_types = {
            "xpath": By.XPATH,
            "id": By.ID,
            "css": By.CSS_SELECTOR,
            "name": By.NAME,
            "link_text": By.LINK_TEXT,
        }

        if locator_type in locator_types:
            return locator_types[locator_type]
        logging.error("Noe supported %s", self.locator_info)
        return False

    def get_element(
        self, locator: str, locator_type: str = "id"
    ) -> Union[WebElement, None]:
        """Sample method docstring - todo"""

        element = None
        try:
            type_of_locator = self.get_by_type(locator_type=locator_type)
            element = self.driver.instance.find_element(
                by=type_of_locator, value=locator
            )
            logging.info(
                "Found element with locator: %s and locator type: %s",
                locator,
                locator_type,
            )
        except NoSuchElementException:
            logging.error(
                "Not found element with locator %s and locator type: %s",
                locator,
                locator_type,
            )
        return element

    def get_elements(
        self, locator: str, locator_type: str = "xpath"
    ) -> Union[WebElement, None]:
        """Sample method docstring - todo"""

        elements = None
        try:
            element_type = self.get_by_type(locator_type=locator_type)
            elements = self.driver.instance.find_elements(
                by=element_type, value=locator
            )
            logging.info(
                "Found elements with locator: %s and locator type: %s",
                locator,
                locator_type,
            )
        except NoSuchElementException:
            logging.error(
                "Not found elements with locator: %s and locator type: %s",
                locator,
                locator_type,
            )
        return elements

    def click_element(self, locator: str, locator_type: str = "xpath") -> bool:
        """Sample method docstring - todo"""

        try:
            element = self.get_element(locator=locator, locator_type=locator_type)
            element.click()
            logging.info(
                "Clicked on element with locator: %s and locator type: %s",
                locator,
                locator_type,
            )
            return True
        except AttributeError:
            logging.error(
                "Not clicked element with locator: %s and locator type: %s",
                locator,
                locator_type,
            )
            return False
        except ElementClickInterceptedException:
            logging.error(
                "Not found element with locator: %s and locator type: %s",
                locator,
                locator_type,
            )
            return False

    def send_keys_to(
        self, locator: str, data: str, locator_type: str = "xpath"
    ) -> None:
        """Sample method docstring - todo"""

        try:
            element = self.get_element(locator=locator, locator_type=locator_type)
            element.send_keys(data)
            logging.info("Data was sent to %s", self.locator_info)
        except AttributeError:
            logging.error("Data NOT sent to %s", self.locator_info)
        except NoSuchElementException:
            logging.error("Not found %s", self.locator_info)

    def is_element_present(self, locator: str, locator_type: str = "xpath") -> bool:
        """Sample method docstring - todo"""

        try:
            element = self.get_element(locator, locator_type)
            if element is not None:
                logging.info("Found %s", self.locator_info)
                return True
            logging.debug("Not found %s", self.locator_info)
            return False
        except ElementNotVisibleException:
            logging.error("Not found %s", self.locator_info)
            return False

    def wait_for_element_appearance(
        self,
        locator: str,
        locator_type: str = "xpath",
        timeout: int = 10,
        click: bool = False,
    ) -> Union[WebElement, None]:
        """Sample method docstring - todo"""
        element = None
        self.driver.instance.implicitly_wait(0)

        try:
            by_type = self.get_by_type(locator_type)
            self.get_element(locator, locator_type)
            logging.info(
                "Waiting for %s for maximum %s seconds", self.locator_info, time
            )

            wait = WebDriverWait(
                driver=self.driver.instance,
                timeout=timeout,
                poll_frequency=0.1,
                ignored_exceptions=[
                    NoSuchElementException,
                    ElementNotVisibleException,
                    ElementNotSelectableException,
                ],
            )

            element = wait.until(EC.element_to_be_clickable((by_type, locator)))

            if click is not False:
                logging.info("Clicking element with locator: %s")
                element.click()

            logging.info("Appeared on the web page an %s", self.locator_info)
            return element

        except TimeoutException:
            logging.error("Exception occurred while waiting for%s", self.locator_info)
        except ElementNotInteractableException:
            logging.error("Error occurred while waiting for%s", self.locator_info)
        except Exception as exc:
            logging.error(
                "Unexpected error occurred while waiting for %s. %s",
                self.locator_info,
                exc,
            )
        finally:
            self.driver.instance.implicitly_wait(self.driver.default_implicitly_wait)
        return element

    def wait_for_element_disappearance(
        self, locator: str, locator_type: str = "xpath", timeout: int = 10
    ) -> bool:
        """Sample method docstring - todo"""

        result = False
        self.driver.instance.implicitly_wait(0)

        try:
            by_type = self.get_by_type(locator_type=locator_type)
            wait = WebDriverWait(
                driver=self.driver.instance, timeout=timeout, poll_frequency=0.1
            )
            disappeared = wait.until(
                EC.invisibility_of_element_located((by_type, locator))
            )
            if disappeared is not False:
                logging.info("Successfully disappeared %s", self.locator_info)
                result = True
            else:
                logging.error("Not disappeared %s", self.locator_info)
        except TimeoutException:
            logging.error("Error occurred %s", self.locator_info)
        finally:
            self.driver.instance.implicitly_wait(self.driver.default_implicitly_wait)
        return result

    def check_if_element_is_not_displayed(
        self, locator: str, locator_type: str = "xpath"
    ) -> bool:
        """Sample method docstring - todo"""

        locator_type = self.get_by_type(locator_type=locator_type)
        try:
            self.driver.instance.find_element(
                by=locator_type, value=locator
            ).is_displayed()
        except NoSuchElementException:
            logging.info("Successfully not displayed %s", self.locator_info)
            return True
        else:
            logging.error("Unwanted displayed %s", self.locator_info)
            return False

    def clear_textarea(self, locator: str) -> None:
        """Sample method docstring - todo"""

        self.send_keys_to(locator=locator, data=Keys.CONTROL + "a")
        self.send_keys_to(locator=locator, data=Keys.DELETE)
