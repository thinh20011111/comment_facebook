import logging

def setup_logger():
    # Cấu hình logger cho terminal
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)  # Chỉ log những lỗi ERROR và CRITICAL vào terminal

    # Cấu hình logger cho file (lưu tất cả log)
    file_handler = logging.FileHandler('error.log', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)  # Ghi tất cả mức độ log (DEBUG, INFO, WARNING, ERROR, CRITICAL) vào file

    # Định dạng log
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Thêm handlers vào logger
    logging.basicConfig(
        level=logging.DEBUG,  # Ghi tất cả mức độ log, nhưng handler quyết định sẽ ghi gì
        handlers=[console_handler, file_handler]
    )
