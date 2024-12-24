from utils.base_page import BasePage
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from utils.config import Config
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import logging
import json
import chardet

logging.basicConfig(
    filename='error.log',
    level=logging.DEBUG,  # Ghi lại tất cả thông tin debug, info, warning, error, critical
    format='%(asctime)s - %(levelname)s - %(message)s',  # Cấu trúc mặc định
    datefmt='%d/%m/%Y %H:%M:%S',  # Định dạng ngày tháng giờ theo kiểu Việt Nam
    encoding='utf-8'  # Đảm bảo rằng file log được ghi với encoding UTF-8
)

def main():
    # Load cấu hình
    config = Config()

    # Khởi tạo Service với đường dẫn ChromeDriver
    service = Service(config.CHROME_DRIVER_PATH)
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")  # Chặn thông báo
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Đọc tệp JSON chứa danh sách tài khoản và bình luận
    accounts_filename = "data/accounts_emso.json"
    facebook_accounts_filename = "data/accounts.json"
    pages_filename = "data/pages.json"

    def load_json_file(filename):
        # Tự động phát hiện encoding và mở tệp
        with open(filename, 'rb') as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
        
        # Mở tệp với encoding phát hiện được
        with open(filename, 'r', encoding=encoding) as file:
            return json.load(file)

    try:
        accounts_data = load_json_file(accounts_filename)
        facebook_data = load_json_file(facebook_accounts_filename)  # Dữ liệu tài khoản Facebook
        pages_data = load_json_file(pages_filename)
        
        accounts = accounts_data  # Dữ liệu tài khoản lấy từ accounts_emso.json
        facebook_accounts = facebook_data.get("accounts", [])  # Tài khoản Facebook lấy từ file
        pages = pages_data.get("pages", [])  # Các trang cần tạo

        if not facebook_accounts:
            logging.error(f"Không có tài khoản Facebook nào trong danh sách!")
            return

        base_page = BasePage(driver)

        # Lấy tài khoản đầu tiên từ file Facebook
        first_facebook_account = facebook_accounts[0]
        print(f"first: {first_facebook_account}")
        
        email = first_facebook_account.get("email")
        print(f"email: {email}")
        password = first_facebook_account.get("password")
        print(f"password: {password}")

        if not email or not password:
            logging.error(f"Tài khoản Facebook đầu tiên thiếu thông tin: {first_facebook_account}")
            return

        try:
            # Đăng nhập vào Facebook với tài khoản đầu tiên
            driver.get(config.FACEBOOK_URL)
            base_page.login_facebook(email, password)

            for page_url in pages:
                # Lặp qua các tài khoản EMSo nếu gặp lỗi tạo trang
                for account in accounts:
                    emso_email = account.get("username")
                    emso_password = account.get("password")

                    try:
                        base_page.create_page_from_facebook(emso_email, emso_password, page_url)
                        break

                    except Exception as e:
                        logging.error(f"Lỗi xảy ra trên trang {page_url} với tài khoản EMSo {emso_email}: {e}")
                        base_page.logout_emso()
                        # Nếu lỗi xảy ra khi tạo trang, chuyển sang tài khoản khác

        except Exception as e:
            logging.error(f"Lỗi đăng nhập Facebook với tài khoản {email}: {e}")
            return  # Nếu lỗi đăng nhập, dừng lại không thử các tài khoản khác

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
