from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

import time
from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = os.getenv("IG_USERNAME")
PASSWORD = os.getenv("IG_PASSWORD")


SIMILAR_ACCOUNT = "therock" # Change this to an account of your choice


class InstaFollower:

    def __init__(self):
        # Keep browser open so you can manually log out
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    # Avoid bot-like behaviour and try not to run your script too often.
    def login(self):
        url = "https://www.instagram.com/accounts/login/"
        self.driver.get(url)
        time.sleep(4.2)

        # Check if the cookie warning is present on the page
        decline_cookies_xpath = "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[2]"
        cookie_warning = self.driver.find_elements(By.XPATH, decline_cookies_xpath)
        if cookie_warning:
            # Dismiss the cookie warning by clicking an element or button
            cookie_warning[0].click()

        username = self.driver.find_element(by=By.NAME, value="email")
        password = self.driver.find_element(by=By.NAME, value="pass")

        username.send_keys(USERNAME)
        password.send_keys(PASSWORD)

        time.sleep(2.1)
        password.send_keys(Keys.ENTER)

        time.sleep(4.3)
        # Click "Not now" and ignore Save-login info prompt
        save_login_prompt = self.driver.find_element(by=By.XPATH, value="//div[contains(text(), 'Not now')]")
        if save_login_prompt:
            save_login_prompt.click()

        time.sleep(3.7)

    def find_followers(self):
        time.sleep(3)
        self.driver.get(f"https://www.instagram.com/{SIMILAR_ACCOUNT}/")
        time.sleep(3)

        # Click the followers link
        followers_link = self.wait.until(
            ec.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/followers')]"))
        )
        followers_link.click()

        # Wait for the modal to appear
        modal = self.wait.until(
            ec.presence_of_element_located(
                (By.XPATH, "//div[@role='dialog']//div[contains(@style, 'overflow')]")
            )
        )

        # Scroll enough to load at least 15 users
        for _ in range(6):
            self.driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight", modal
            )
            time.sleep(1.5)

    def follow(self):
        # Find all visible "Follow" buttons
        follow_buttons = self.driver.find_elements(By.XPATH, "//div[text()='Follow']")

        count = 0

        for btn in follow_buttons:
            if count >= 15:
                break

            try:
                btn.click()
                count += 1
                time.sleep(1.2)

            except ElementClickInterceptedException:
                # Handle "Cancel" popup
                try:
                    cancel = self.driver.find_element(
                        By.XPATH, "//button[contains(text(), 'Cancel')]"
                    )
                    cancel.click()
                except:
                    pass

        print(f"Followed {count} people.")


bot = InstaFollower()
bot.login()
bot.find_followers()
bot.follow()