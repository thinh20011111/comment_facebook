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
    INFOR = "//div[@class='jss48 MuiBox-root css-fstzj5']//i[contains(@class, 'fa-solid fa-angle-down')]"
    LOG_OUT = "//p[normalize-space(text())='Đăng xuất']"
    COMMENT_IN_DETAIL = "(//div[@contenteditable='true' and @role='textbox'])[4]"
    
    PAGE_CREATE_PAGE_TITLE_INPUT = "//textarea[@name='title']"
    PAGE_CREATE_PAGE_PURPOSE_DROPDOWN = "//input[@name='page_purpose']"
    PAGE_CREATE_PAGE_TYPE_DROPDOWN = "//input[@name='page_type']"
    PAGE_CREATE_PAGE_CATEGORY_DROPDOWN = "//input[@name='page_category_ids']"
    PAGE_CREATE_PAGE_DESCRIPTION_TEXTAREA = "//textarea[@name='description']"
    PAGE_CREATE_PAGE_CREATE_BUTTON = "//button[./div[text()='Tạo trang']]"
    PAGE_CREATE_PAGE_PURPOSE_OPTION = "//p[text()='{purpose}']"
    PAGE_CREATE_PAGE_TYPE_PERSONEL_OPTION = "//p[text()='Cá nhân']"
    PAGE_CREATE_PAGE_TYPE_COMPANY_OPTION = "//p[text()='Doanh nghiệp']"
    PAGE_CREATE_PAGE_CATEGORY_LANSCAPE_OPTION = "//div[text()='Trang web giải trí']"
    PAGE_CREATE_CLOSE_BUTTON = "//*[name()='svg' and @data-testid='ClearIcon']"
    AVATAR = "//input[@type='file' and @name='avatar' and @accept='image/jpeg,image/png,image/jpg']"
    BANNER = "//input[@type='file' and @name='banner' and @accept='image/jpeg,image/png,image/jpg']"
    CREATE_PAGE = "//button[@id='demo-customized-button' and contains(., 'Tạo trang')]"
    TOAST = "//div[@class='MuiAlert-message css-1w0ym84']"
    OPEN_FORM_USERNAME = "//a[contains(text(), 'Tạo @')]"
    INPUT_USERNAME_PAGE = "//textarea[@id='username' and @name='username' and @placeholder='Tên người dùng']"
    UPDATE_USERNAME_BUTTON = "//div[@class='MuiBox-root css-80hrfn' and text()='Cập nhật']"
    LOGOUT_BTN = "//header//div[@role= 'button' and ./div/p[text()='Đăng xuất']]"
    AVATAR_FACEBOOK = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[1]"
    BANNER_FACEBOOK = "//img[@data-imgperflogname='profileCoverPhoto']"
    AVATAR_FACEBOOK_DOWLOAD = "/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div[2]/div/div[2]/div/div[1]/div/div[2]/div/div/div/img"
    PAGES_LEFT_MENU = "//main/div/div[1]/div[2]/div[1]/nav/a[7]"
    VIEW_AVATAR_OPTION = "//a[contains(@class, 'x1i10hfl') and contains(., 'Xem ảnh đại diện')]"
    CONFIRM_LOGOUT = "//button//div[normalize-space(text())='Rời khỏi']"
    CONFIRM_CREATE = "//button[.//div[normalize-space(text())='Xong']]"
    
    def find_element(self, locator_type, locator_value):
        return self.driver.find_element(locator_type, locator_value)
    
    def login_facebook(self, username, password):
        self.input_text(self.INPUT_USERNAME, username)
        self.input_text(self.INPUT_PASSWORD, password)
        self.click_element(self.LOGIN_BUTTON) 
        time.sleep(5)
    
    def login_emso(self, username = str, password = str):
        self.input_text(self.LOGIN_EMAIL_INPUT, username)
        self.input_text(self.LOGIN_PWD_INPUT, password)
        self.click_element(self.LOGIN_SUBMIT_BTN)
        self.wait_for_element_clickable(self.PROFILE_ACCOUNT_ICON)
    
    def logout_emso(self):
        self.click_element(self.PROFILE_ACCOUNT_ICON)
        self.click_element(self.LOGOUT_BTN)
        self.driver.get(self.config.EMSO_URL)
    
    def logout(self):
        self.click_element(self.INFOR)
        self.click_element(self.LOG_OUT)
    
    def logout_when_create_page(self):
        self.click_element(self.INFOR)
        self.click_element(self.LOG_OUT)
        self.click_element(self.CONFIRM_LOGOUT)
        
    def is_element_present_by_xpath(self, xpath: str) -> bool:
        try:
            # Tìm phần tử bằng XPath
            self.driver.find_element(By.XPATH, xpath)
            return True
        except NoSuchElementException:
            # Nếu không tìm thấy phần tử, trả về False
            return False
    
    def verify_text_from_element(self, element_locator, expected_text):
        try:
            # Lấy văn bản của phần tử
            actual_text = self.get_text_from_element(element_locator)

            # Kiểm tra xem văn bản có khớp với giá trị mong muốn không
            if actual_text.strip() == expected_text.strip():
                logging.info(f"Văn bản khớp: '{actual_text}'")
                return True
            else:
                logging.error(f"Văn bản không khớp. Mong đợi: '{expected_text}', Thực tế: '{actual_text}'")
                return False
        except Exception as e:
            logging.error(f"Lỗi khi kiểm tra văn bản từ phần tử {element_locator}: {e}")
            return False  # Trả về False nếu có lỗi    

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
    
    def create_page(self, pagename, page_username, avatar, banner):
        # Điền tên trang
        self.input_text(self.PAGE_CREATE_PAGE_TITLE_INPUT, pagename)
        # Chọn mục "Trang nội dung"
        self.click_element(self.PAGE_CREATE_PAGE_PURPOSE_DROPDOWN)
        self.click_element(self.PAGE_CREATE_PAGE_PURPOSE_OPTION.replace('{purpose}', "Trang nội dung"))
        # Chọn loại trang
        self.click_element(self.PAGE_CREATE_PAGE_TYPE_DROPDOWN)
        self.click_element(self.PAGE_CREATE_PAGE_TYPE_PERSONEL_OPTION)
        # Chọn danh mục
        self.click_element(self.PAGE_CREATE_PAGE_CATEGORY_DROPDOWN)
        self.input_text(self.PAGE_CREATE_PAGE_CATEGORY_DROPDOWN, "Trang web giải trí")
        
        time.sleep(2)
        # Chọn mục "Trang web giải trí"
        self.click_element(self.PAGE_CREATE_PAGE_CATEGORY_LANSCAPE_OPTION)
        # Điền mô tả trang
        self.input_text(self.PAGE_CREATE_PAGE_DESCRIPTION_TEXTAREA, "Mô tả trang")
        # Tải ảnh đại diện và ảnh bìa
        self.upload_image(self.AVATAR, avatar)
        self.upload_image(self.BANNER, banner)
        # Nhấn nút tạo trang
        time.sleep(3)
        self.click_element(self.PAGE_CREATE_PAGE_CREATE_BUTTON)

        time.sleep(2)
        if self.is_element_present_by_xpath(self.TOAST):
            toast = self.find_element_by_locator(self.TOAST)
            logging.error(f"Lỗi khi tạo trang {pagename}: {toast.text}")
            return False  # Trả về False nếu có lỗi
        else:
            # Cập nhật username của trang
            self.click_element(self.OPEN_FORM_USERNAME)
            self.input_text(self.INPUT_USERNAME_PAGE, page_username)
            self.click_outside_input(self.INPUT_USERNAME_PAGE)
            time.sleep(1)
            self.click_element(self.UPDATE_USERNAME_BUTTON)
            self.click_element(self.CONFIRM_CREATE)
            logging.info(f"Đã tạo trang thành công: {pagename}")
            return True  # Trả về True nếu tạo trang thành công

    def save_to_csv(self, page_username, username, password):
        # Đường dẫn tới file CSV
        file_path = "data/pageES.csv"
        facebook_url = f"https://www.facebook.com/{page_username}"
        emso_url = f"https://{self.config.EVN}-fe.emso.vn/page/{page_username}"

        # Kiểm tra và tạo file nếu chưa tồn tại
        file_exists = os.path.exists(file_path)
        
        # Mở file CSV để lưu kết quả
        with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Facebook URL', 'EMSO URL', 'Username', 'Password']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Ghi header nếu file chưa tồn tại
            if not file_exists:
                writer.writeheader()

            # Ghi thông tin vào CSV
            writer.writerow({
                'Facebook URL': facebook_url,
                'EMSO URL': emso_url,
                'Username': username,
                'Password': password
            })

        logging.info(f"Đã lưu thông tin trang {page_username} vào file CSV tại {file_path}.")

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
                image = Image.open(BytesIO(response.content))
                
                # Kiểm tra kích thước ảnh
                if image.width < 450 or image.height < 150:
                    # Resize ảnh để đạt kích thước tối thiểu
                    new_width = max(450, image.width)
                    new_height = max(150, image.height)
                    image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    print(f"Image resized to {new_width}x{new_height}")

                # Lưu ảnh vào tệp
                image.save(filepath)
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
            banner_img_path = None
            banner_img_tag = self.driver.find_element(By.XPATH, self.BANNER_FACEBOOK)
            banner_url = banner_img_tag.get_attribute('src') if banner_img_tag else None
            if banner_url:
                banner_img_path = f"{username}_banner.jpg"
                self.download_image(banner_url, banner_img_path)

            # Tải ảnh avatar
            avatar_img_path = None
            self.click_element(self.AVATAR_FACEBOOK)

            time.sleep(2)
            
            if self.is_element_present_by_xpath(self.VIEW_AVATAR_OPTION):
                self.click_element(self.VIEW_AVATAR_OPTION)
            else:
                print("[!] VIEW_AVATAR_OPTION không tồn tại hoặc không hiển thị.")

            try:
                avatar_img_tag = WebDriverWait(self.driver, 50).until(
                    EC.presence_of_element_located((By.XPATH, self.AVATAR_FACEBOOK_DOWLOAD))
                )
                
                if avatar_img_tag:
                    outer_html = avatar_img_tag.get_attribute("outerHTML")

                    avatar_url = avatar_img_tag.get_attribute('src')

                    if avatar_url and avatar_url.startswith("http"):
                        avatar_img_path = f"{username}_avatar.jpg"
                        self.download_image(avatar_url, avatar_img_path)
                    else:
                        print("[!] Không tìm thấy hoặc URL ảnh không hợp lệ.")
                else:
                    print("[!] Không tìm thấy thẻ ảnh avatar.")
                    
            except Exception as e:
                import traceback
                print("[!] Lỗi khi lấy avatar:")
                traceback.print_exc()

            # Chuẩn bị dữ liệu để lưu
            page_info = {
                'page_name': page_name,
                'username': username,
                'banner_img_path': banner_img_path,
                'avatar_img_path': avatar_img_path
            }

            # Đường dẫn file JSON
            json_file_path = "data/data_page.json"

            # Kiểm tra và đọc dữ liệu cũ từ file JSON (nếu có)
            if os.path.exists(json_file_path):
                with open(json_file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
            else:
                data = {}

            # Cập nhật dữ liệu theo `username`
            data[username] = page_info

            # Ghi lại dữ liệu vào file JSON
            with open(json_file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            return page_info

        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def download_video_from_xpath(self, url, xpath, output_file):
        try:
            # Tìm phần tử video qua XPath
            video_element = self.driver.find_element(By.XPATH, xpath)
            video_url = video_element.get_attribute("src")

            if not video_url:
                raise Exception("Không tìm thấy URL video.")

            print(f"Đang tải video từ: {video_url}")

            # Tải video bằng requests
            response = requests.get(video_url, stream=True)
            if response.status_code == 200:
                with open(output_file, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        f.write(chunk)
                print(f"Video đã được lưu tại: {output_file}")
            else:
                raise Exception(f"Lỗi tải video: HTTP {response.status_code}")
        except Exception as e:
            print(f"Lỗi: {e}")
        