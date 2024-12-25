from utils.base_page import BasePage
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from utils.config import Config
from selenium.webdriver.chrome.options import Options
import time
import random
import logging
import json
import chardet  # Dùng để tự động phát hiện encoding tệp
from itertools import cycle  # Lặp lại danh sách tài khoản
from logger_config import setup_logger


def main():
    # Load cấu hình
    config = Config()
    setup_logger()

    # Khởi tạo Service với đường dẫn ChromeDriver
    service = Service(config.CHROME_DRIVER_PATH)
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")  # Chặn thông báo
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Đọc tệp JSON chứa danh sách tài khoản và bình luận
    accounts_filename = "data/accounts.json"
    comments_filename = "data/comments.json"
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
        comments_data = load_json_file(comments_filename)
        pages_data = load_json_file(pages_filename)

        accounts = accounts_data.get("accounts", [])
        comments = comments_data.get("comments", [])
        pages = pages_data.get("pages", [])

        if not accounts or not comments or not pages:
            logging.error("Danh sách tài khoản, bình luận hoặc trang trống.")
            return

        # Kiểm tra danh sách tài khoản và URL có đủ không
        if len(accounts) < len(pages):
            logging.warning("Số lượng tài khoản ít hơn số lượng trang, sẽ lặp lại tài khoản.")
        
        base_page = BasePage(driver)

        # Lặp qua các tài khoản và trang
        for account, page_url in zip(cycle(accounts), pages):  # Sử dụng cycle để lặp lại tài khoản
            email = account.get("email")
            password = account.get("password")

            if not email or not password:
                logging.warning(f"Tài khoản thiếu thông tin: {account}")
                continue

            try:
                # Mở trang web và đăng nhập
                driver.get(config.FACEBOOK_URL)
                base_page.login_facebook(email, password)

                # Lấy bình luận ngẫu nhiên
                comment_text = random.choice(comments)

                # Điều hướng đến trang và thực hiện bình luận
                base_page.go_to_page_and_comment(page_url, comment_text)

                # Đăng xuất
                base_page.logout()

            except Exception as e:
                logging.error(f"Lỗi xảy ra với tài khoản {email} trên trang {page_url}: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
