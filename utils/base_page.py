from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
import os
import logging
from PIL import Image
from io import BytesIO
import csv
import pandas as pd
import requests
import json
import time

class BasePage:
    def __init__(self, driver):
        self.driver = driver
    
    INPUT_USERNAME = "//input[@id='email']"
    INPUT_PASSWORD = "//input[@id='pass']"    
    LOGIN_BUTTON = "//button[text()='Log in']"
    INPUT_COMMENT_TEMPLATE = "(//div[@class='xzsf02u x1a2a7pz x1n2onr6 x14wi4xw notranslate' and @contenteditable='true'])[{index}]"
    BUTTON_COMMENT = "/html/body/div[1]/div/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[2]/div[3]/div[{index}]/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[4]/div/div/div[1]/div/div[2]/div/div[2]"
    VIEW_DETAIL_POST = "/html/body/div[1]/div/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[2]/div[3]/div[{index}]/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[4]/div/div/div/div/div[1]/div/div[2]/div[2]/span"
    SEND_COMMENT = "(//div[@aria-label='Bình luận'])[{index}]"
    BUTTON_SHOW_COMMENT = "(//div[contains(@class, 'x9f619')]/div[contains(@class, 'x1n2onr6')]/span/span[text()='Bình luận'])[{index}]"
    INFOR = "//div[@aria-label='Trang cá nhân của bạn' and contains(@class, 'x1i10hfl') and @role='button']"
    LOG_OUT = "//span[contains(@class, 'x193iq5w') and text()='Đăng xuất']"
    COMMENT_IN_DETAIL = "(//div[@contenteditable='true' and @role='textbox'])[4]"

    def find_element(self, locator_type, locator_value):
        return self.driver.find_element(locator_type, locator_value)
    
    def login_facebook(self, username, password):
        self.input_text(self.INPUT_USERNAME, username)
        self.input_text(self.INPUT_PASSWORD, password)
        self.click_element(self.LOGIN_BUTTON) 
        time.sleep(5)
    
    def logout(self):
        self.click_element(self.INFOR)
        self.click_element(self.LOG_OUT)
        
    def is_element_present_by_xpath(self, xpath: str) -> bool:
        try:
            # Tìm phần tử bằng XPath
            self.driver.find_element(By.XPATH, xpath)
            return True
        except NoSuchElementException:
            # Nếu không tìm thấy phần tử, trả về False
            return False
    
    def click_element(self, xpath: str, timeout=15):
        try:
            element = self.wait_for_element_clickable(xpath, timeout)
            # Cuộn đến phần tử nếu cần
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            element.click()
            logging.info(f"Clicked on element with XPath: {xpath}")
        except Exception as e:
            logging.error(f"Error while clicking element with XPath '{xpath}': {e}")
            raise
        
    def wait_for_element_clickable(self, xpath: str, timeout=15):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
        except TimeoutException:
            logging.error(f"Element with XPath '{xpath}' not clickable after {timeout} seconds.")
            raise
     
    def input_text(self, xpath: str, text: str):
        try:
            # Chờ phần tử khả dụng
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )

            # Tìm phần tử và cuộn tới nó
            element = self.driver.find_element(By.XPATH, xpath)
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()

            # Đảm bảo phần tử hiện hữu và không bị thay đổi trạng thái
            for _ in range(3):  # Thử tối đa 3 lần nếu có lỗi StaleElementReferenceException
                try:
                    # Chờ phần tử khả dụng lại nếu cần
                    WebDriverWait(self.driver, 3).until(EC.visibility_of(element))
                    
                    # Xóa văn bản hiện tại
                    element.click()
                    element.send_keys(Keys.CONTROL + "a")  # Chọn tất cả văn bản
                    element.send_keys(Keys.DELETE)  # Xóa văn bản cũ
                    
                    # Nhập văn bản mới
                    element.send_keys(text)
                    return  # Thành công, thoát khỏi hàm
                except StaleElementReferenceException:
                    # Reload phần tử nếu DOM thay đổi
                    element = self.driver.find_element(By.XPATH, xpath)
            raise Exception("Không thể tương tác với phần tử sau nhiều lần thử.")
        except TimeoutException:
            logging.error("Phần tử không sẵn sàng hoặc không khả dụng trong thời gian chờ.")
        except Exception as e:
            logging.error(f"Không thể nhập văn bản vào phần tử: {e}")
    
    def get_text_from_element(self, locator):
        try:
            text = self.driver.find_element(By.XPATH, locator).text
            return text
        except Exception as e:
            logging.error(f"Error getting text from element with XPath '{locator}': {e}")
            return ""
    
    def get_data_from_json_file(self, file_name):
        data_file = f'{file_name}.json'
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f, strict=False)
            return data
        except Exception as e:
            logging.error(f"Error reading JSON file {data_file}: {e}")
            return {}
   
    def wait_for_element_present(self, locator, timeout=15):
        WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, locator)))
        return self.find_element_by_locator(locator)

    def find_element_by_locator(self, locator, context=None):
        try:
            if context:
                element = context.find_element(By.XPATH, locator)
            else:
                element = self.driver.find_element(By.XPATH, locator)
            return element
        except Exception as e:
            logging.error(f"Error finding element by locator '{locator}': {e}")
            return None

    def scroll_until_element_found(self, xpath, max_scrolls=10):
        """
        Cuộn trang đến khi phần tử được tìm thấy hoặc đạt đến số lần cuộn tối đa.
        :param xpath: XPath của phần tử cần tìm.
        :param max_scrolls: Số lần cuộn tối đa để tìm phần tử.
        """
        scroll_count = 0
        while scroll_count < max_scrolls:
            try:
                # Tìm phần tử với XPath
                element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                # Nếu phần tử tìm thấy, trả về phần tử
                return element
            except:
                # Nếu không tìm thấy, cuộn trang xuống dưới
                self.driver.execute_script("window.scrollBy(0, 300);")
                time.sleep(2)  # Đợi một chút để trang tải thêm
                scroll_count += 1
        # Nếu không tìm thấy sau max_scrolls lần cuộn, trả về None
        return None

    def check_and_open_modal(self):
        try:
            # Cuộn đến phần tử "Bình luận" đầu tiên
            comment_button = self.scroll_until_element_found("//span[contains(text(),'Bình luận')]")
            if comment_button:
                comment_button.click()

                # Chờ modal xuất hiện
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true' and @role='textbox']"))
                )
        except Exception as e:
            print(f"Lỗi khi mở modal hoặc tìm nút bình luận: {e}")

    def enter_comment(self, comment_text):
        try:
            # Tìm ô nhập bình luận trong modal
            comment_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true' and @role='textbox']"))
            )

            # Nhập nội dung bình luận vào ô comment
            comment_box.send_keys(comment_text)

            # Gửi bình luận (nhấn Enter)
            comment_box.send_keys(Keys.RETURN)

            # Đợi một chút để bình luận được gửi
            time.sleep(3)
            print("Bình luận đã được gửi thành công!")

        except Exception as e:
            print(f"Lỗi khi gửi bình luận: {e}")
            
    def press_enter(driver, element_xpath):
        try:
            element = driver.find_element(By.XPATH, element_xpath)
            element.send_keys(Keys.RETURN)  # or use Keys.ENTER
        except Exception as e:
            logging.error(f"Error pressing enter on element with XPath '{element_xpath}': {e}")
    
    def go_to_page_and_comment(self, page_url, comment_text):
        try:
            self.driver.get(page_url)
            self.check_and_open_modal()
            self.enter_comment(comment_text)
            self.driver.back()
        except Exception as e:
            logging.error(f"Error navigating to page {page_url} and posting comment: {e}")
    
    def enter_text(self, xpath, text, wait_time=1):
        try:
            input_element = self.driver.find_element(By.XPATH, xpath)
            input_element.clear()
            input_element.send_keys(text)
            time.sleep(wait_time)  # Optional: Wait to ensure actions are completed
            logging.info(f"Entered text: {text}")
        
        except Exception as e:
            logging.error(f"An error occurred while entering text: {e}")
    
