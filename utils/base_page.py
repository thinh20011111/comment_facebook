from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
import os
from bs4 import BeautifulSoup
import logging
from PIL import Image
from io import BytesIO
import csv
import pandas as pd
import requests
import json
from utils.config import Config
import time

class BasePage:
    def __init__(self, driver):
        self.config = Config()
        self.driver = driver
    
    INPUT_USERNAME = "//input[@id='email']"
    INPUT_PASSWORD = "//input[@id='pass']"    
    LOGIN_BUTTON = "//button[text()='Log in']"
    LOGIN_EMAIL_INPUT = "//input[@id='email' and @type='text']"
    LOGIN_PWD_INPUT = "//input[@id='password' and @type='password']"
    LOGIN_SUBMIT_BTN = "//button[@id='demo-customized-button' and ./div[text()='Đăng nhập']]"
    PROFILE_ACCOUNT_ICON = "//div[@id='root']/div/div/div/div/header/div/div/div[3]/div/div[2]/div[2]/i"
    INPUT_COMMENT_TEMPLATE = "(//div[@class='xzsf02u x1a2a7pz x1n2onr6 x14wi4xw notranslate' and @contenteditable='true'])[{index}]"
    BUTTON_COMMENT = "/html/body/div[1]/div/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[2]/div[3]/div[{index}]/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[4]/div/div/div[1]/div/div[2]/div/div[2]"
    VIEW_DETAIL_POST = "/html/body/div[1]/div/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[2]/div[3]/div[{index}]/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[4]/div/div/div/div/div[1]/div/div[2]/div[2]/span"
    SEND_COMMENT = "(//div[@aria-label='Bình luận'])[{index}]"
    BUTTON_SHOW_COMMENT = "(//div[contains(@class, 'x9f619')]/div[contains(@class, 'x1n2onr6')]/span/span[text()='Bình luận'])[{index}]"
    INFOR = "//div[@aria-label='Trang cá nhân của bạn' and contains(@class, 'x1i10hfl') and @role='button']"
    LOG_OUT = "//span[contains(@class, 'x193iq5w') and text()='Đăng xuất']"
    COMMENT_IN_DETAIL = "(//div[@contenteditable='true' and @role='textbox'])[4]"
    
    INPUT_PAGE_NAME = "//textarea[@id='title' and @name='title' and @placeholder='Thông tin về trang']"
    INPUT_PAGE_PURPOSE = "//input[@name='page_purpose' and @type='text' and @id='mui-66']"
    OPTION_PAGE_PURPOSE = "//p[contains(text(),'Trang nội dung')]"
    INPUT_TYPE_PAGE = "//input[@name='page_type' and @type='text' and @id='mui-68']"
    OPTION_TYPE_PAGE = "//p[contains(text(),'Cá nhân')]"
    INPUT_PAGE_CATEGORY = "//input[@name='page_category_ids' and @type='text' and @id='mui-70']"
    OPTION_PAGE_CATEGORY = "//div[@id='mui-70-option-0']//div[1]"
    PAGE_DESCRIPTION = "//textarea[@id='description' and @name='description' and @placeholder='Thêm mô tả ngắn' and @rows='4']"
    AVATAR = "//input[@type='file' and @name='avatar' and @accept='image/jpeg,image/png,image/jpg']"
    BANNER = "//input[@type='file' and @name='banner' and @accept='image/jpeg,image/png,image/jpg']"
    CREATE_PAGE = "//button[@id='demo-customized-button' and contains(., 'Tạo trang')]"
    TOAST = "//div[@class='MuiAlert-message css-1w0ym84']"
    OPEN_FORM_USERNAME = "//a[contains(text(), 'Tạo @')]"
    INPUT_USERNAME_PAGE = "//textarea[contains(@class, 'MuiInputBase-input') and @placeholder='Tên người dùng']"
    UPDATE_USERNAME_BUTTON = "//div[@class='MuiBox-root css-80hrfn' and text()='Cập nhật']"
    LOGOUT_BTN = "//header//div[@role= 'button' and ./div/p[text()='Đăng xuất']]"
    AVATAR_FACEBOOK = "/html/body/div[1]/div/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[1]/div"
    
    def find_element(self, locator_type, locator_value):
        return self.driver.find_element(locator_type, locator_value)
    
    def login_facebook(self, username, password):
        self.input_text(self.INPUT_USERNAME, username)
        self.input_text(self.INPUT_PASSWORD, password)
        self.click_element(self.LOGIN_BUTTON) 
        time.sleep(5)
    
    def login_emso(self, username, password):
        self.driver.get(self.config.EMSO_URL)
        time.sleep(1)
        self.input_text(self.LOGIN_EMAIL_INPUT, username)
        self.input_text(self.LOGIN_PWD_INPUT, password)
        self.click_element(self.LOGIN_SUBMIT_BTN)
        self.wait_for_element_clickable(self.PROFILE_ACCOUNT_ICON)
    
    def logout_emso(self):
        self.click_element(self.PROFILE_ACCOUNT_ICON)
        self.click_element(self.LOGOUT_BTN)
    
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

    def click_outside_input(self, element):
        try:
            body = self.driver.find_element(By.TAG_NAME, 'body')
            action = ActionChains(self.driver)
            action.move_to_element(body).click().perform()
        except Exception as e:
            print(f"Error clicking outside input: {e}")
    
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
    
    def upload_image(self, file_input_locator, image_name):
        try:
            # Kiểm tra nếu image_name là một danh sách, nếu có, lấy phần tử đầu tiên
            if isinstance(image_name, list):
                image_name = image_name[0]  # Lấy ảnh đầu tiên trong danh sách

            # Đảm bảo đường dẫn tuyệt đối tới thư mục 'media' và ảnh
            media_dir = os.path.join(os.getcwd(), 'media')  # Lấy đường dẫn tuyệt đối thư mục 'media'
            image_path = os.path.join(media_dir, image_name)  # Đảm bảo đường dẫn chính xác

            # In ra đường dẫn ảnh để kiểm tra
            print(f"Đường dẫn ảnh: {image_path}")

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
    
    def create_page_emso(self, page_name, page_description, banner, avatar, page_username):
        try:
            self.input_text(self.INPUT_PAGE_NAME, page_name)
            self.click_element(self.INPUT_PAGE_PURPOSE)
            self.click_element(self.OPTION_PAGE_PURPOSE)
            self.click_element(self.INPUT_TYPE_PAGE)
            self.click_element(self.OPTION_TYPE_PAGE)
            self.click_element(self.INPUT_PAGE_CATEGORY)
            self.click_element(self.OPTION_PAGE_CATEGORY)
            self.input_text(self.PAGE_DESCRIPTION, page_description)
            self.upload_image(self.AVATAR, avatar)
            self.upload_image(self.BANNER, banner)
            self.click_element(self.CREATE_PAGE)
            
            # Kiểm tra nếu phần tử thông báo lỗi (TOAST) xuất hiện
            toast = self.find_element("//div[@class='MuiAlert-message css-1w0ym84']")
            if toast:
                # Nếu có thông báo lỗi, ghi lại lỗi và có thể ném exception
                logging.error(f"Lỗi khi tạo trang: {toast.text}")
                raise Exception(f"Lỗi khi tạo trang: {toast.text}")
            
            self.click_element(self.OPEN_FORM_USERNAME)
            self.input_text(self.INPUT_USERNAME, page_username)
            self.click_outside_input(self.INPUT_USERNAME)
            self.click_element(self.UPDATE_USERNAME_BUTTON)
        except Exception as e:
            logging.error(f"Đã xảy ra lỗi khi tạo trang: {e}")
            raise  # Ném lại lỗi nếu cần thiết để xử lý tiếp
    
    def download_image(self, url, filename):
        try:
            # Đảm bảo thư mục media tồn tại
            media_folder = "media"
            if not os.path.exists(media_folder):
                os.makedirs(media_folder)  # Tạo thư mục nếu chưa tồn tại
            
            # Lấy đường dẫn đầy đủ cho tệp ảnh
            filepath = os.path.join(media_folder, filename)
            
            # Tải ảnh
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                print(f"Downloaded image: {filepath}")
            else:
                print(f"Failed to download image from {url}")
        except Exception as e:
            print(f"Error downloading image: {e}")

    # Hàm truy cập vào trang Facebook và lấy thông tin
    def get_facebook_page_info(self, page_url):
        try:
            # Truy cập vào URL trang Facebook
            self.driver.get(page_url)
            time.sleep(3)  # Đợi trang tải xong

            # Lấy tên của trang
            page_name = self.driver.find_element(By.TAG_NAME, 'h1').text.strip()

            # Lấy username từ URL
            username = page_url.split('/')[-1]  # Username ở cuối URL

            # Tải ảnh banner
            banner_img_tag = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[1]/div/div/div/div[2]/div/a/div[1]/div/div/div/img")
            if banner_img_tag:
                banner_url = banner_img_tag.get_attribute('src')
                if banner_url:
                    self.download_image(banner_url, 'banner.jpg')

            # Tải ảnh avatar
            # Click vào phần tử avatar Facebook
            self.click_element(self.AVATAR_FACEBOOK)
            
            # Đợi phần tử hình ảnh tải xong (10 giây tối đa)
            avatar_img_tag = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//img[@class='x1bwycvy x193iq5w x4fas0m x19kjcj4' and @data-visualcompletion='media-vc-image']"))
            )

            # Lấy URL ảnh avatar
            avatar_url = avatar_img_tag.get_attribute('src')
            
            if avatar_url:
                # Tải ảnh xuống thư mục media
                self.download_image(avatar_url, 'avatar.jpg')

            # Lấy phần giới thiệu (text)
            description = ''
            try:
                description_tag = self.driver.find_element(By.XPATH, "//div[@data-pagelet='ProfileIntroduction']")
                if description_tag:
                    description = description_tag.text.strip()
            except Exception as e:
                print("No description found.")

            return {
                'page_name': page_name,
                'username': username,
                'description': description
            }

        except Exception as e:
            print(f"Error: {e}")
            return None

    def create_page_from_facebook(self, username, password, page_url):
        """Lấy thông tin trang Facebook và tạo trang emso."""
        try:
            # Lấy thông tin trang từ Facebook
            page_info = self.get_facebook_page_info(page_url)
            print(f"page: {page_info}")
            self.driver.get(self.config.EMSO_URL)
            self.login_emso(username, password)
            self.driver.get(self.config.EMSO_CREATE_PAGE_URL)
            # Truyền các thông tin này vào hàm create_page_emso
            self.create_page_emso(
                page_name=page_info['username'],
                page_description=page_info['description'],
                banner=page_info['banner'],
                avatar=page_info['avatar'],
                page_username=page_info['username']
            )
            self.logout_emso()
        except Exception as e:
            logging.error(f"Không thể tạo trang từ Facebook: {e}")
            raise