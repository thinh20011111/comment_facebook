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

def save_error_page(page_url, reason):
    with open("data/error_page.txt", "a", encoding="utf-8") as f:
        f.write(f"{page_url} | {reason}\n")

def load_json_file(filename):
    # Tự động phát hiện encoding
    with open(filename, 'rb') as file:
        raw_data = file.read()
        encoding = chardet.detect(raw_data)['encoding']
    
    with open(filename, 'r', encoding=encoding) as file:
        return json.load(file)

def main():
    # Load cấu hình
    config = Config()
    setup_logger()

    service = Service(config.CHROME_DRIVER_PATH)
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Load dữ liệu
    facebook_accounts = load_json_file("data/accounts.json").get("accounts", [])
    pages = load_json_file("data/pages.json").get("pages", [])
    emso_accounts_data = load_json_file("data/accounts_emso.json")

    if not facebook_accounts or not pages:
        logging.error("Thiếu tài khoản Facebook hoặc danh sách page.")
        return

    emso_accounts = list(emso_accounts_data.items())
    remaining_pages = pages.copy()

    try:
        base_page = BasePage(driver)

        # Đăng nhập Facebook một lần duy nhất
        fb_email = facebook_accounts[0].get("email")
        fb_password = facebook_accounts[0].get("password")

        if not fb_email or not fb_password:
            logging.error("Thiếu thông tin tài khoản Facebook.")
            return

        print(f"Đăng nhập Facebook: {fb_email}")
        driver.get(config.FACEBOOK_URL)
        base_page.login_facebook(fb_email, fb_password)
        time.sleep(50)

        emso_index = 0

        while remaining_pages and emso_index < len(emso_accounts):
            account_key, account_data = emso_accounts[emso_index]
            emso_email = account_data["username"]
            emso_password = account_data["password"]

            try:
                print(f"\nĐăng nhập EMSO với tài khoản: {emso_email}")
                driver.get(config.EMSO_URL)
                base_page.login_emso(emso_email, emso_password)
                time.sleep(2)

                while remaining_pages:
                    page_url = remaining_pages[0]
                    try:
                        page_info = base_page.get_facebook_page_info(page_url)
                        if not page_info:
                            save_error_page(page_url, "Không lấy được thông tin page")
                            remaining_pages.pop(0)
                            continue

                        page_name = page_info.get("page_name")
                        page_username = page_info.get("username")
                        avatar = page_info.get("avatar_img_path")
                        banner = page_info.get("banner_img_path")

                        if not banner:
                            save_error_page(page_url, "Lỗi tải banner")
                            remaining_pages.pop(0)
                            continue

                        if not avatar:
                            save_error_page(page_url, "Lỗi tải avatar")
                            remaining_pages.pop(0)
                            continue

                        print(f"➡️ Tạo page: {page_name} ({page_username})")
                        driver.get(config.EMSO_CREATE_PAGE_URL)

                        try:
                            success = base_page.create_page(page_name, page_username, avatar, banner)
                        except Exception as upload_err:
                            save_error_page(page_url, "Lỗi upload avatar/banner")
                            break  # chuyển tài khoản emso

                        if success:
                            base_page.save_to_csv(page_username, emso_email, emso_password)
                            print(f"✅ Thành công: {page_username}")
                            remaining_pages.pop(0)
                        else:
                            save_error_page(page_url, "Tạo page thất bại")
                            break  # chuyển tài khoản emso

                    except Exception as page_error:
                        save_error_page(page_url, f"Lỗi không xác định: {str(page_error)}")
                        break  # chuyển tài khoản emso

                base_page.logout_emso()

            except Exception as account_error:
                logging.error(f"Lỗi tài khoản EMSO {account_key}: {account_error}")

            emso_index += 1  # Sang tài khoản tiếp theo nếu bị lỗi

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
