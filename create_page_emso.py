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
import json
import chardet
import logging
from logger_config import setup_logger

def main():
    # Load cấu hình
    config = Config()
    setup_logger()

    # Khởi tạo Service với đường dẫn ChromeDriver
    service = Service(config.CHROME_DRIVER_PATH)
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Chế độ không giao diện
    chrome_options.add_argument("--disable-notifications")  # Chặn thông báo
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Đọc tệp JSON chứa danh sách tài khoản và bình luận
    facebook_accounts_filename = "data/accounts.json"
    pages_filename = "data/pages.json"
    accounts_filename = "data/accounts_emso.json"
    pages_crawl_filename = "data/data_page.json"

    with open(accounts_filename, 'r') as file:
        accounts_data = json.load(file)
    
    with open(pages_crawl_filename, "r", encoding="utf-8") as file:
        pages_crawl_data = json.load(file)
    
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
        facebook_data = load_json_file(facebook_accounts_filename)  # Dữ liệu tài khoản Facebook
        pages_data = load_json_file(pages_filename)

        facebook_accounts = facebook_data.get("accounts", [])  # Tài khoản Facebook lấy từ file
        pages = pages_data.get("pages", [])  # Các trang cần tạo
        pages_crawl = pages_crawl_data
        
        if not facebook_accounts:
            logging.error(f"Không có tài khoản Facebook nào trong danh sách!")
            return

        base_page = BasePage(driver)

        # Lấy tài khoản đầu tiên từ file Facebook
        first_facebook_account = facebook_accounts[0]
        
        email = first_facebook_account.get("email")
        password = first_facebook_account.get("password")

        if not email or not password:
            logging.error(f"Tài khoản Facebook đầu tiên thiếu thông tin: {first_facebook_account}")
            return
       
        # try:
        #     driver.get(config.FACEBOOK_URL)
        #     base_page.login_facebook(email, password)

        #     for page_url in pages:
        #         try:
        #             # Lấy thông tin trang Facebook
        #             page_info = base_page.get_facebook_page_info(page_url)
        #             if page_info:
        #                 logging.info(f"Thông tin trang: {page_info}")
        #             else:
        #                 logging.warning(f"Không thể lấy thông tin trang: {page_url}")
        #         except Exception as page_error:
        #             logging.error(f"Lỗi khi xử lý trang {page_url}: {page_error}")
        #             continue  # Chuyển sang trang tiếp theo nếu lỗi
            
        #     print(pages_crawl)
        # except Exception as e:
        #     logging.error(f"Lỗi đăng nhập Facebook với tài khoản {email}: {e}")
        #     return  # Nếu lỗi đăng nhập, dừng lại không thử các tài khoản khác
     
        
        failed_pages = []

        for account_key, account_data in accounts_data.items():
            try:
                print(f"\nĐang xử lý tài khoản: {account_key}")
                email = account_data["username"]  # Đảm bảo 'username' tồn tại trong dictionary
                password = account_data["password"]  # Đảm bảo 'password' tồn tại trong dictionary

                # Đăng nhập vào tài khoản hiện tại
                driver.get(config.EMSO_URL)
                base_page.login_emso(email, password)

                # Xử lý tất cả các trang trong pages_crawl_data
                pages_to_create = failed_pages if failed_pages else pages_crawl_data.items()
                failed_pages = []  # Đặt lại danh sách lỗi cho tài khoản hiện tại

                for page_key, pages_crawl in pages_to_create:
                    page_name = pages_crawl["page_name"]
                    page_username = pages_crawl["username"]
                    banner = pages_crawl["banner_img_path"]
                    avatar = pages_crawl["avatar_img_path"]
                    print(f"Đang tạo trang: {page_name}, {page_username}")

                    # Tạo trang
                    driver.get(config.EMSO_CREATE_PAGE_URL)
                    success = base_page.create_page(page_name, page_username, avatar, banner)
                    print(success)
                    if success:
                        base_page.save_to_csv(page_username, email, password)  # Lưu vào CSV
                        print(f"Tạo thành công trang: {page_name} ({page_username})")
                    else:
                        # Nếu không thành công, thêm vào danh sách lỗi
                        print(f"Lỗi khi tạo trang: {page_name}.")
                        failed_pages.append((page_key, pages_crawl))

                # In thông báo khi hoàn thành xử lý tài khoản
                print(f"Hoàn thành xử lý cho tài khoản: {email}")
                base_page.logout_emso()  # Đăng xuất khi hoàn thành
            except Exception as account_error:
                logging.error(f"Lỗi khi xử lý tài khoản {account_key}: {account_error}")
                continue  # Tiếp tục với tài khoản tiếp theo

        if failed_pages:
            print("Các trang chưa được tạo:")
            for page_key, pages_crawl in failed_pages:
                print(f"- {pages_crawl['page_name']} ({pages_crawl['username']})")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
