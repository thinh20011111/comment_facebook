import csv
import json
import os

def csv_to_json(csv_file, json_file):
    # Kiểm tra xem file JSON đã tồn tại hay chưa, nếu có thì xóa
    if os.path.exists(json_file):
        os.remove(json_file)

    # Đọc file CSV
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)  # Sử dụng DictReader để đọc với header làm key
        urls = []

        # Đọc từng dòng trong file CSV và chỉ lấy dữ liệu từ cột A (cột đầu tiên)
        for row in reader:
            url = row[list(row.keys())[0]]  # Lấy giá trị từ cột đầu tiên
            urls.append(url)  # Thêm URL vào danh sách

    # Định dạng dữ liệu theo yêu cầu
    output = {"urls": urls}

    # Ghi dữ liệu vào file JSON
    with open(json_file, mode='w', encoding='utf-8') as jsonf:
        json.dump(output, jsonf, indent=4, ensure_ascii=False)

# Ví dụ sử dụng hàm
csv_to_json('data_page.csv', 'account.json')
