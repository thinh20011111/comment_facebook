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
    chrome_options.add_argument("--headless")  # Chế độ không giao diện
    chrome_options.add_argument("--disable-notifications")  # Chặn thông báo
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    base_page = BasePage()
    try:
        base_page.download_video_from_xpath(url, xpath, output_file)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
