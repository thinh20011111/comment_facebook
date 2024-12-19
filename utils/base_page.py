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

logging.basicConfig(
    filename='error.log', 
    level=logging.ERROR, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class BasePage:
    def __init__(self, driver):
        self.driver = driver
    
    INPUT_USERNAME = "//input[@id='email']"
    INPUT_PASSWORD = "//input[@id='pass']"    
    LOGIN_BUTTON = "//button[text()='Log in']"
    LOGIN_PWD_INPUT = "//input[@id='password' and @type='password']"
    LOGIN_SUBMIT_BTN = "//button[@id='demo-customized-button' and ./div[text()='Đăng nhập']]"
    PROFILE_ACCOUNT_ICON = "//div[@id='root']/div/div/div/div/header/div/div/div[3]/div/div[2]/div[2]/i"
    LOGOUT_BTN = "//header//div[@role= 'button' and ./div/p[text()='Đăng xuất']]"
    
    def find_element(self, locator_type, locator_value):
        return self.driver.find_element(locator_type, locator_value)
    
    def login_facebook(self, username, password):
        self.input_text(self.INPUT_USERNAME, username)
        self.input_text(self.INPUT_PASSWORD, password)
        self.click_element(self.LOGIN_BUTTON) 
        time.sleep(5)
    
    def login_emso(self, url, username, password):
        self.driver.get(url)
        time.sleep(1)
        self.input_text(self.LOGIN_EMAIL_INPUT, username)
        self.input_text(self.LOGIN_PWD_INPUT, password)
        self.click_element(self.LOGIN_SUBMIT_BTN)
        self.wait_for_element_clickable(self.PROFILE_ACCOUNT_ICON)
        
    def logout(self):
        self.click_element(self.PROFILE_ACCOUNT_ICON)
        self.click_element(self.LOGOUT_BTN)
        
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
            # print(f"Clicked on element with XPath: {xpath}")
        except Exception as e:
            print(f"Error while clicking element with XPath '{xpath}': {e}")
            raise
        
    def wait_for_element_clickable(self, xpath: str, timeout=15):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
        except TimeoutException:
            print(f"Element with XPath '{xpath}' not clickable after {timeout} seconds.")
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
            print("Phần tử không sẵn sàng hoặc không khả dụng trong thời gian chờ.")
        except Exception as e:
            print(f"Không thể nhập văn bản vào phần tử: {e}")
    
    def get_text_from_element(self, locator):
        text = self.driver.find_element(By.XPATH, locator).text
        return text
    
    def get_data_from_json_file(self, file_name):
        data_file = f'{file_name}.json'
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f, strict = False)
        return data

    def upload_image(self, file_input_locator, image_name):
        try:
            # Kiểm tra nếu image_name là một danh sách, nếu có, lấy phần tử đầu tiên
            if isinstance(image_name, list):
                image_name = image_name[0]  # Lấy ảnh đầu tiên trong danh sách

            # Xác định đường dẫn tuyệt đối của ảnh trong thư mục media
            image_path = os.path.abspath(f"media/{image_name}")  # Thư mục media và tên tệp ảnh

            # Kiểm tra xem file có tồn tại không
            if not os.path.exists(image_path):
                print(f"File không tồn tại: {image_path}")
                return

            # Tìm phần tử input và gửi đường dẫn ảnh
            file_input = self.wait_for_element_present(file_input_locator)
            file_input.send_keys(image_path)

            print(f"Đã upload ảnh: {image_path}")

        except Exception as e:
            print(f"Error uploading image: {e}")
        
    def wait_for_element_present(self, locator, timeout=15):
        WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, locator)))
        return self.find_element_by_locator(locator)

    def find_element_by_locator(self, locator, context=None):
        if context:
            element = context.find_element(By.XPATH, locator)
        else:
            element = self.driver.find_element(By.XPATH, locator)
        return element

    def read_accounts_from_json(self, filename):
        with open(filename, 'r') as file:
            accounts_data = json.load(file)
        return accounts_data

    # Đọc các bài viết từ file facebook_posts.json
    def read_posts_from_json(self, filename, pagename):
        with open(filename, 'r') as file:
            posts_data = json.load(file)
        return posts_data.get(pagename, [])

    # Đăng bài lên Facebook (giả định)
    def create_post(self, title, image_name):
        # Mở form tạo bài đăng
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, self.OPEN_FORM)))  # Ensure post loads
        self.click_element(self.OPEN_FORM)

        # Nhập tiêu đề bài đăng
        self.input_text(self.INPUT_POST, title)

        # Tải lên ảnh (nếu có)
        self.upload_image(self.INPUT_MEDIA, image_name)

        # Nhấn nút đăng bài
        self.click_element(self.CREATE_POST_BUTTON)
        time.sleep(5)  # Đợi một chút để quá trình đăng bài hoàn tất
    
    # # Hàm chính kiểm tra và đăng bài
    # def process_post(self, group_url, accounts_filename, posts_filename):
    #     # Trích xuất Page Name từ URL
    #     pagename = group_url.split("/")[-1]  # Lấy phần cuối của URL để làm page name

    #     # Đọc dữ liệu tài khoản từ file JSON
    #     accounts_data = self.read_accounts_from_json(accounts_filename)

    #     # Kiểm tra nếu pagename có trong tài khoản
    #     if pagename in accounts_data:
    #         print(f"Trang {pagename} có trong tài khoản, bắt đầu đăng bài.")

    #         # Đọc các bài viết từ file facebook_posts.json
    #         posts = self.read_posts_from_json(posts_filename, pagename)

    #         # Đăng tất cả các bài viết của trang
    #         for post in posts:
    #             # Lấy tiêu đề bài đăng
    #             title = post.get("title", "")

    #             # Lấy đường dẫn ảnh từ trường "media"
    #             image_paths = post.get("media", [])

    #             # Thực hiện đăng bài
    #             self.create_post(title, self.FILE_INPUT_LOCATOR, image_paths)
    #     else:
    #         print(f"Trang {pagename} không tồn tại trong tài khoản.")